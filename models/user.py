from google.appengine.ext import db


class User(db.Model):
    """A class to hold user details"""
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
