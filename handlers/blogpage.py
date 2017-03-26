from models import BlogPost
from handler import Handler
from google.appengine.ext import db


class BlogPageHandler(Handler):
    """A class to retrieve all blog posts."""

    def get(self):
        user = self.validate_user()
        # get all blog entries from db
        blog_entries = db.Query(BlogPost).order('-created')
        self.render("blog_page.html", blog_entries=blog_entries,
                    user=user)
