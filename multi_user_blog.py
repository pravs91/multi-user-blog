import webapp2
from handlers import *

app = webapp2.WSGIApplication([
    ('/', MainPage),
    (r'/blog/?', BlogPageHandler),
    (r'/blog/signup/?', SignUpHandler),
    (r'/blog/login/?', LoginHandler),
    (r'/blog/welcome/?', WelcomeHandler),
    (r'/blog/newpost/?', NewPostHandler),
    (r'/blog/(\d+)/?', PermalinkHandler),
    (r'/blog/logout/?', LogoutHandler),
    (r'/blog/(\d+)/edit', EditPageHandler),
    (r'/blog/(\d+)/delete', DeletePageHandler),
    (r'/blog/(\d+)/createComment', CreateCommentHandler),
    (r'/blog/(\d+)/editComment', EditCommentHandler),
    (r'/blog/(\d+)/deleteComment', DeleteCommentHandler),
    (r'/blog/(\w+)/?', UserBlogPageHandler)  # check if a user page exists
], debug=True)
