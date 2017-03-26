from models import BlogPost, User, Comment
from handler import Handler
from google.appengine.ext import db


class DeletePageHandler(Handler):
    """A class to delete a blog post"""

    def get(self, blog_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # retrieve blog and show delete page
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
            # render delete_success page
            self.render("delete_success.html", subject=subject, user=user)
        else:
            self.error_404("The requested blog URL was not found.")
