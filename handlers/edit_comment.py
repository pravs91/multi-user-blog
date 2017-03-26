from models import BlogPost, User, Comment
from handler import Handler, CommentsHelper
from google.appengine.ext import db


class EditCommentHandler(Handler):
    """A class to edit a comment."""

    def get(self, comment_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # retrieve comment and pre-populate fields
        comment = Comment.get_by_id(int(comment_id))
        if comment:
            blog_entries = [comment.blog]
            comments_dict = CommentsHelper.populate_comments(blog_entries)
            self.render("create_comment.html", user=user,
                        content=comment.content, permalink=True,
                        blog_entries=blog_entries,
                        comments_dict=comments_dict)
        else:
            self.error_404("The requested comment URL does not exist.")

    def post(self, comment_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # retrieve comment and edit
        comment = Comment.get_by_id(int(comment_id))
        if comment:
            comment.content = self.request.get("comment")
            comment.put()
            # time.sleep(0.2)
            blog_id = comment.blog.key().id()
            self.redirect('/blog/' + str(blog_id))
        else:
            self.error_404("The requested comment URL does not exist.")
