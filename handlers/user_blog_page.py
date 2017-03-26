from models import BlogPost, User
from handler import Handler
from google.appengine.ext import db


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
        blog_entries = given_user.blog_entries.order('-created')
        logged_in_user = self.validate_user()
        self.render("user_blog_page.html",
                    blog_entries=blog_entries,
                    user=logged_in_user, username=username)
