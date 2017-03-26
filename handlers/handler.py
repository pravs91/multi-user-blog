import os
import webapp2
import jinja2
import time
from utilities import check_cookie
from models import User, Comment
from google.appengine.ext import db

handlers_path = os.path.dirname(__file__)
template_dir = os.path.join(os.path.dirname(handlers_path), 'templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    "A class to handle common functionality of subclasses"

    # write the response
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    # render a template
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    # gets the cookie and checks if it is valid
    # delete cookie if it is wrong/tampered
    # returns user instance if valid cookie found
    def validate_user(self):
        cookie = self.request.cookies.get('user')
        id = cookie and check_cookie(cookie)
        if id:
            user = User.get_by_id(int(id))
            return user
        else:
            # delete cookie if it exists (means it has been tampered)
            if cookie:
                self.response.headers.add_header('Set-Cookie', 'user=; Path=/')
            return None

    # return 404 response with error msg
    def error_404(self, msg):
        self.response.status = '404 Not found'
        self.response.body = 'Error 404! ' + msg


class CommentsHelper(object):

    # helper method to populate comments of each blog in a dict
    @staticmethod
    def populate_comments(blog_entries):
        comments_dict = {}
        for blog in blog_entries:
            # retrieve comments for this blog
            comments = db.Query(Comment).filter(
                'blog =', blog).order('created')
            # populate dict with id as unique key
            # if comments exist for this blog
            if comments.count(limit=2) > 0:
                comments_dict[blog.key().id()] = comments
        return comments_dict
