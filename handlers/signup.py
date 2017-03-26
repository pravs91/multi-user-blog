from google.appengine.ext import db
from models import User
from handler import Handler
from utilities import make_pw_hash, make_cookie
import re


class SignUpHandler(Handler):
    """A class to handle signup page."""

    # regex to validate user inputs
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"[\S]+@[\S]+.[\S]+$")

    def get(self):
        self.render("user_signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        invalid_username = None
        username_exists = None
        invalid_password = None
        passwords_dont_match = None
        invalid_email = None

        valid_username = self.validate(self.USER_RE, username)
        if not valid_username:
            invalid_username = "That's not a valid username."

        # check if username already exists in db
        all_users = db.Query(User).filter('username =', username)
        user = all_users.get()
        if user:
            username_exists = "That username already exists."

        valid_password = self.validate(self.PASSWORD_RE, password)
        if not valid_password:
            invalid_password = "That wasn't a valid password."

        passwords_match = (verify == password)
        if valid_password and (not passwords_match):
            passwords_dont_match = "Your passwords didn't match."

        if email:
            valid_email = self.validate(self.EMAIL_RE, email)
            if not valid_email:
                invalid_email = "That's not a valid email."

        if invalid_username or username_exists or invalid_password or\
                invalid_email or passwords_dont_match:
            # populate all error msgs in dict
            kwargs = {'invalid_username': invalid_username,
                      'username_exists': username_exists,
                      'invalid_password': invalid_password,
                      'passwords_dont_match': passwords_dont_match,
                      'invalid_email': invalid_email,
                      'username': username,
                      'email': email
                      }
            self.render("user_signup.html", **kwargs)
        else:
            # create User instance and put into db
            pw_hash = make_pw_hash(username, password)
            newuser = User(username=username, pw_hash=pw_hash, email=email)
            newuser.put()  # put into User db
            key = newuser.key().id()
            # set cookie
            cookie = make_cookie(str(key))
            self.response.headers.add_header(
                'Set-Cookie', 'user=%s; Path=/' % cookie)
            return self.redirect("/blog/welcome")

    def validate(self, reObj, input):
        return reObj.match(input)
