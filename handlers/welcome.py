from models import BlogPost
from handler import Handler, CommentsHelper
from google.appengine.ext import db


class WelcomeHandler(Handler):
    """A class to show welcome page to logged in user."""

    def get(self):
        # this function will delete cookie if it is not valid
        user = self.validate_user()
        if user:
            # get blog entries of this particular user from db
            blog_entries = db.Query(BlogPost).filter(
                'user =', user).order('-created')
            # populate comments for the blogs
            comments_dict = CommentsHelper.populate_comments(blog_entries)
            self.render("welcome_page.html", user=user,
                        blog_entries=blog_entries,
                        comments_dict=comments_dict)
        else:
            self.redirect("/blog/login")
