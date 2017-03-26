from models import BlogPost, User, Comment
from handler import Handler, CommentsHelper
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
            blog_entries = [comment.blog]
            comments_dict = CommentsHelper.populate_comments(blog_entries)
            self.render("delete_comment.html", comment=comment, user=user,
                        blog_entries=blog_entries, comments_dict=comments_dict,
                        permalink=True)
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
            blog_id = comment.blog.key().id()
            comment.delete()
            # time.sleep(0.2)
            self.redirect('/blog/' + str(blog_id))
        else:
            self.error_404("The requested comment URL does not exist.")
