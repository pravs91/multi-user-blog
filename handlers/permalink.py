from models import BlogPost, Comment
from handler import Handler
from google.appengine.ext import db


class PermalinkHandler(Handler):
    """A class to show a permalink for a blog."""

    def get(self, blog_id):
        # retrieve blog from db
        blog = BlogPost.get_by_id(int(blog_id))
        if blog:
            user = self.validate_user()
            blog_entries = [blog]  # user array to use same template
            self.render("blog_entries.html",
                        blog_entries=blog_entries, user=user,
                        permalink=True)
        # send 404 if not found
        else:
            self.error_404("The requested blog URL was not found.")
