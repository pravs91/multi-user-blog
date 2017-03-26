from google.appengine.ext import db
from user import User
from blogpost import BlogPost


class Like(db.Model):
    # Not used for now, try to extend project to count Likes
    blog = db.ReferenceProperty(BlogPost)
    user = db.ReferenceProperty(User)
