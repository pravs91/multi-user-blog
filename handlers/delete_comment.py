from models import BlogPost, User, Comment
from handler import Handler
from google.appengine.ext import db


class DeleteCommentHandler(Handler):
    """A class to delete a comment."""

    def get(self, comment_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # retrieve comment to display on top
        comment = Comment.get_by_id(int(comment_id))
        if comment:
            # check if comment belongs to user
            if comment.user.username != user.username:
                return self.redirect('/blog/login')

            blog_entries = [comment.blog]
            self.render("delete_comment.html", comment=comment, user=user,
                        blog_entries=blog_entries, permalink=True)
        else:
            self.error_404("The requested comment URL does not exist.")

    def post(self, comment_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # retrieve comment and delete if exists
        comment = Comment.get_by_id(int(comment_id))
        if comment:
            # check if comment belongs to user
            if comment.user.username != user.username:
                return self.redirect('/blog/login')

            blog_id = comment.blog.key().id()
            comment.delete()
            # time.sleep(0.2)
            self.redirect('/blog/' + str(blog_id))
        else:
            self.error_404("The requested comment URL does not exist.")
