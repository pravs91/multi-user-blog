from google.appengine.ext import db


class User(db.Model):
    username = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)


class BlogPost(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)  # post create/edit date
    user = db.ReferenceProperty(User)


class Like(db.Model):
    blog = db.ReferenceProperty(BlogPost)
    user = db.ReferenceProperty(User)


class Comment(db.Model):
    blog = db.ReferenceProperty(BlogPost)
    user = db.ReferenceProperty(User)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)  # create/edit date
