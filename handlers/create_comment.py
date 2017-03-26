from models import BlogPost, User, Comment
from handler import Handler, CommentsHelper
from google.appengine.ext import db


class CreateCommentHandler(Handler):
    """A class to create comments for a blog post"""

    def get(self, blog_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # retrieve blog and comments
        blog = BlogPost.get_by_id(int(blog_id))
        if blog:
            blog_entries = [blog]
            comments_dict = CommentsHelper.populate_comments(blog_entries)
            self.render("create_comment.html", user=user, permalink=True,
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
            # create comment and insert into db
            comment = Comment(user=user, blog=blog, content=content)
            comment.put()
            # time.sleep(0.2)  # hack for localhost consistency
            self.redirect('/blog/' + blog_id)
        else:
            self.error_404("The requested blog URL was not found.")
