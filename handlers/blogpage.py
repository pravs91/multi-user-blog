from models import BlogPost
from handler import Handler, CommentsHelper
from google.appengine.ext import db


class BlogPageHandler(Handler):
    """A class to retrieve all blog posts."""

    def get(self):
        user = self.validate_user()
        # get all blog entries from db
        blog_entries = db.Query(BlogPost).order('-created')

        # populate comments for all blogs
        comments_dict = CommentsHelper.populate_comments(blog_entries)
        self.render("blog_page.html", blog_entries=blog_entries,
                    user=user, comments_dict=comments_dict)
