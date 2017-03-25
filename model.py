from google.appengine.ext import db


class User(db.Model):
    """A class to hold user details"""
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class BlogPost(db.Model):
    """A class to hold blog post details"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)  # create/edit date
    user = db.ReferenceProperty(User)  # user for this blog post


class Like(db.Model):
    # Not used for now, try to extend project to count Likes
    blog = db.ReferenceProperty(BlogPost)
    user = db.ReferenceProperty(User)


class Comment(db.Model):
    """A class to hold a comment associated with a blog."""
    blog = db.ReferenceProperty(BlogPost)  # blog for the comment
    user = db.ReferenceProperty(User)  # user who posted the comment
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)  # create/edit date
