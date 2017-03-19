# a module for utility methods used in the app
import random
import string
import hashlib
import hmac

SECRET = "IAmSoCoolButThisIsASecret"


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(7))


def make_pw_hash(username, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(username + pw + salt).hexdigest()
    return "%s|%s" % (h, salt)


def validate_pw(username, pw, h):
    salt = h.split('|')[1]
    if h == make_pw_hash(username, pw, salt):
        return True


def make_cookie(id):
    h = hmac.new(SECRET, id).hexdigest()
    return "%s|%s" % (id, h)


def check_cookie(cookie):
    id = cookie.split('|')[0]
    if cookie == make_cookie(id):
        return id
