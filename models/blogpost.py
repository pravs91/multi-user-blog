from google.appengine.ext import db
from user import User


class BlogPost(db.Model):
    """A class to hold blog post details"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)  # create/edit date
    # user for this blog post
    user = db.ReferenceProperty(User, collection_name='blog_entries')
