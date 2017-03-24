import os
import webapp2
import jinja2
import re
import time
from utilities import make_salt, make_pw_hash, validate_pw,\
    make_cookie, check_cookie
from model import User, BlogPost, Like, Comment
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    "A class to handle common functionality of subclasses"

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # gets the cookie and checks if it is valid
    # delete cookie if it is wrong/tampered
    # returns user instance if valid cookie found
    def validate_user(self):
        cookie = self.request.cookies.get('user')
        id = cookie and check_cookie(cookie)
        if id:
            user = User.get_by_id(int(id))
            return user
        else:
            # delete cookie if it exists (means it has been tampered)
            if cookie:
                self.response.headers.add_header('Set-Cookie', 'user=; Path=/')
            return None

    def error_404(self, msg):
        self.response.status = '404 Not found'
        self.response.body = 'Error 404! ' + msg


class SignUpHandler(Handler):
    """A class to handle signup page."""

    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"[\S]+@[\S]+.[\S]+$")

    def get(self):
        self.render("user_signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        invalid_username = None
        username_exists = None
        invalid_password = None
        passwords_dont_match = None
        invalid_email = None

        valid_username = self.validate(self.USER_RE, username)
        if not valid_username:
            invalid_username = "That's not a valid username."

        all_users = db.Query(User).filter('username =', username)
        user = all_users.get()
        if user:
            username_exists = "That username already exists."

        valid_password = self.validate(self.PASSWORD_RE, password)
        if not valid_password:
            invalid_password = "That wasn't a valid password."

        passwords_match = (verify == password)
        if valid_password and (not passwords_match):
            passwords_dont_match = "Your passwords didn't match."

        if email:
            valid_email = self.validate(self.EMAIL_RE, email)
            if not valid_email:
                invalid_email = "That's not a valid email."

        if invalid_username or username_exists or invalid_password or\
                invalid_email or passwords_dont_match:
            kwargs = {'invalid_username': invalid_username,
                      'username_exists': username_exists,
                      'invalid_password': invalid_password,
                      'passwords_dont_match': passwords_dont_match,
                      'invalid_email': invalid_email,
                      'username': username,
                      'email': email
                      }
            self.render("user_signup.html", **kwargs)
        else:
            pw_hash = make_pw_hash(username, password)
            newuser = User(username=username, pw_hash=pw_hash, email=email)
            newuser.put()  # put into User db
            key = newuser.key().id()
            cookie = make_cookie(str(key))
            self.response.headers.add_header(
                'Set-Cookie', 'user=%s; Path=/' % cookie)
            return self.redirect("/blog/welcome")

    def validate(self, reObj, input):
        return reObj.match(input)


class LoginHandler(Handler):
    """A class to handle the login page."""

    def get(self):
        # if the user is already logged in and
        # tries to access the /login page, redirect to /welcome
        user = self.validate_user()
        if user:
            self.redirect("/blog/welcome")

        # render login page otherwise
        self.render("login.html")

    def invalid_login(self, error, username):
        self.render("login.html", error=error, username=username)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        # check if both username and password was entered
        if not (username and password):
            error = "Please enter a valid username and password."
            self.invalid_login(error, username)
            return

        # check if username exists in db
        all_users = db.Query(User).filter('username =', username)
        user = all_users.get()
        if not user:
            error = "The given username is not registered."
            self.invalid_login(error, username)
            return

        # validate user's password using helper method
        # set cookie if password is valid
        pw_hash = user.pw_hash
        if validate_pw(username, password, pw_hash):
            key = user.key().id()
            cookie = make_cookie(str(key))
            self.response.headers.add_header(
                'Set-Cookie', 'user=%s; Path=/' % cookie)
            return self.redirect("/blog/welcome")

        # password is wrong
        else:
            error = "Your password is not correct."
            self.invalid_login(error, username)
            return


class LogoutHandler(Handler):

    # delete cookie and redirect to /login
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user=; Path=/')
        self.redirect("/blog/login")


class NewPostHandler(Handler):

    def get(self):
        # if user is not logged in, redirect to login
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # render newpost page if logged in
        self.render("newpost.html", user=user)

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if not (subject and content):
            error = "Please enter both subject and content."
            self.render("newpost.html", error=error,
                        subject=subject, content=content)
        else:
            user = self.validate_user()
            # redirect to login if cookie wrong
            if not user:
                return self.redirect("/blog/login")
            blog = BlogPost(subject=subject, content=content, user=user)
            blog.put()  # insert into db
            id = blog.key().id()
            self.redirect("/blog/" + str(id))


class MainPage(Handler):

    def get(self):
        self.redirect('/blog')


class CommentsHelper(object):

    @staticmethod
    def populate_comments(blog_entries):
        comments_dict = {}
        for blog in blog_entries:
            # retrieve comments for this blog
            comments = db.Query(Comment).filter(
                'blog =', blog).order('created')
            # populate dict with id as unique key
            if comments.count(limit=2) > 0:
                comments_dict[blog.key().id()] = comments
        return comments_dict


class WelcomeHandler(Handler):
    """A class to show welcome page to logged in user."""

    def get(self):
        # this function will delete cookie if it is not valid
        user = self.validate_user()
        if user:
            # get blog entries of this particular user from db
            blog_entries = db.Query(BlogPost).filter(
                'user =', user).order('-created')
            comments_dict = CommentsHelper.populate_comments(blog_entries)
            self.render("welcome_page.html", user=user,
                        blog_entries=blog_entries,
                        comments_dict=comments_dict)
        else:
            self.redirect("/blog/login")


class PermalinkHandler(Handler):

    def get(self, blog_id):
        blog = BlogPost.get_by_id(int(blog_id))
        if blog:
            user = self.validate_user()
            comments = db.Query(Comment).filter(
                'blog =', blog).order('created')
            blog_entries = [blog]  # user array to use same template
            comments_dict = CommentsHelper.populate_comments(blog_entries)
            self.render("blog_entries.html",
                        blog_entries=blog_entries, user=user,
                        comments_dict=comments_dict)
        # send 404 if not found
        else:
            self.error_404("The requested blog URL was not found.")


class BlogPageHandler(Handler):
    """A class to retrieve all blog posts."""

    def get(self):
        # get all blog entries from db
        user = self.validate_user()
        blog_entries = db.Query(BlogPost).order('-created')
        comments_dict = CommentsHelper.populate_comments(blog_entries)
        self.render("blog_page.html", blog_entries=blog_entries,
                    user=user, comments_dict=comments_dict)


class UserBlogPageHandler(Handler):
    """A class to get the blog page of a particular user."""

    def get(self, username):
        # get user if username exists
        all_users = db.Query(User).filter('username =', username)
        given_user = all_users.get()
        # error 404 if username not found
        if not given_user:
            self.error_404("The requested user's blog was not found.")
            return

        # get blog entries of this particular user from db
        blog_entries = db.Query(BlogPost).filter(
            'user =', given_user).order('-created')
        comments_dict = CommentsHelper.populate_comments(blog_entries)
        logged_in_user = self.validate_user()
        self.render("user_blog_page.html",
                    blog_entries=blog_entries, comments_dict=comments_dict,
                    user=logged_in_user, username=username)


class EditPageHandler(Handler):
    """A class to edit a blog post."""

    def get(self, blog_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")
        blog = BlogPost.get_by_id(int(blog_id))
        if blog:
            self.render("edit_page.html", user=user,
                        subject=blog.subject, content=blog.content)
        # redirect to /blog if post not found
        else:
            self.error_404("The requested blog URL was not found.")

    def post(self, blog_id):
        subject = self.request.get("subject")
        content = self.request.get("content")

        # validate subject and content present
        if not (subject and content):
            error = "Please enter both subject and content."
            self.render("edit_page.html", error=error,
                        subject=subject, content=content)
        else:
            user = self.validate_user()
            # redirect to login if cookie wrong
            if not user:
                return self.redirect("/blog/login")

            # retrieve blog post from db
            blog = BlogPost.get_by_id(int(blog_id))
            if blog:
                blog.subject = subject
                blog.content = content
                blog.put()
                self.redirect('/blog/' + blog_id)
            # 404 error if blog not found
            else:
                self.error_404("The requested blog URL was not found.")


class DeletePageHandler(Handler):

    def get(self, blog_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")
        blog = BlogPost.get_by_id(int(blog_id))
        if blog:
            self.render("delete_page.html", user=user,
                        blog=blog)
        # send 404 error if post not found
        else:
            self.error_404("The requested blog URL was not found.")

    def post(self, blog_id):
        user = self.validate_user()
        # redirect to login if cookie wrong
        if not user:
            return self.redirect("/blog/login")

        # retrieve blog post from db
        blog = BlogPost.get_by_id(int(blog_id))

        # delete and redirect to /blog
        if blog:
            subject = blog.subject
            # delete associated comments
            comments = db.Query(Comment).filter('blog =', blog)
            db.delete(comments)
            # delete blog itself
            blog.delete()
            self.render("delete_success.html", subject=subject, user=user)
        else:
            self.error_404("The requested blog URL was not found.")


class CreateCommentHandler(Handler):

    def get(self, blog_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")
        blog = BlogPost.get_by_id(int(blog_id))
        if blog:
            blog_entries = [blog]
            comments_dict = CommentsHelper.populate_comments(blog_entries)
            self.render("create_comment.html", user=user,
                        blog_entries=blog_entries, comments_dict=comments_dict)
        # send 404 error if post not found
        else:
            self.error_404("The requested blog URL was not found.")

    def post(self, blog_id):
        user = self.validate_user()
        # redirect to login if cookie wrong
        if not user:
            return self.redirect("/blog/login")

        # retrieve blog post from db
        blog = BlogPost.get_by_id(int(blog_id))

        if blog:
            content = self.request.get("comment")
            comment = Comment(user=user, blog=blog, content=content)
            comment.put()
            time.sleep(0.2)  # FIXME comment while deploying
            self.redirect('/blog/' + blog_id)
        else:
            self.error_404("The requested blog URL was not found.")


class EditCommentHandler(Handler):

    def get(self, comment_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        comment = Comment.get_by_id(int(comment_id))
        if comment:
            blog_entries = [comment.blog]
            comments_dict = CommentsHelper.populate_comments(blog_entries)
            self.render("create_comment.html", user=user,
                        content=comment.content,
                        blog_entries=blog_entries,
                        comments_dict=comments_dict)
        else:
            self.error_404("The requested comment URL does not exist.")

    def post(self, comment_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        comment = Comment.get_by_id(int(comment_id))
        if comment:
            comment.content = self.request.get("comment")
            comment.put()
            time.sleep(0.2)  # FIXME
            blog_id = comment.blog.key().id()
            self.redirect('/blog/' + str(blog_id))
        else:
            self.error_404("The requested comment URL does not exist.")


app = webapp2.WSGIApplication([
    ('/', MainPage),
    (r'/blog/?', BlogPageHandler),
    (r'/blog/signup/?', SignUpHandler),
    (r'/blog/login/?', LoginHandler),
    (r'/blog/welcome/?', WelcomeHandler),
    (r'/blog/newpost/?', NewPostHandler),
    (r'/blog/(\d+)/?', PermalinkHandler),
    (r'/blog/logout/?', LogoutHandler),
    (r'/blog/(\d+)/edit', EditPageHandler),
    (r'/blog/(\d+)/delete', DeletePageHandler),
    (r'/blog/(\d+)/createComment', CreateCommentHandler),
    (r'/blog/(\d+)/editComment', EditCommentHandler),
    (r'/blog/(\w+)/?', UserBlogPageHandler)  # check if a user page exists
], debug=True)
