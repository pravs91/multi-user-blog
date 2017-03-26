from google.appengine.ext import db
from user import User
from blogpost import BlogPost


class Comment(db.Model):
    """A class to hold a comment associated with a blog."""
    # blog for the comment
    blog = db.ReferenceProperty(
        BlogPost, collection_name='blog_comments')
    # user who posted the comment
    user = db.ReferenceProperty(User, collection_name='user_comments')
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)  # create/edit date
