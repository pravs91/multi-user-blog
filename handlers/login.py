from google.appengine.ext import db
from utilities import validate_pw, make_cookie
from models import User
from handler import Handler


class LoginHandler(Handler):
    """A class to handle the login page."""

    def get(self):
        # if the user is already logged in and
        # tries to access the /login page, redirect to /welcome
        user = self.validate_user()
        if user:
            self.redirect("/blog/welcome")

        # render login page otherwise
        self.render("login.html")

    # function to redner template with errors
    def invalid_login(self, error, username):
        self.render("login.html", error=error, username=username)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        # check if both username and password was entered
        if not (username and password):
            error = "Please enter a valid username and password."
            self.invalid_login(error, username)
            return

        # check if username exists in db
        all_users = db.Query(User).filter('username =', username)
        user = all_users.get()
        if not user:
            error = "The given username is not registered."
            self.invalid_login(error, username)
            return

        # validate user's password using helper method
        # set cookie if password is valid
        pw_hash = user.pw_hash
        if validate_pw(username, password, pw_hash):
            key = user.key().id()
            cookie = make_cookie(str(key))
            self.response.headers.add_header(
                'Set-Cookie', 'user=%s; Path=/' % cookie)
            return self.redirect("/blog/welcome")

        # password is wrong
        else:
            error = "Your password is not correct."
            self.invalid_login(error, username)
            return
