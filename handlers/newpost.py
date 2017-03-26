from handler import Handler
from models import BlogPost


class NewPostHandler(Handler):
    """A class to handle /newpost request"""

    def get(self):
        # if user is not logged in, redirect to login
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # render newpost page if logged in
        self.render("newpost.html", user=user)

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        # check if both subject and content exist
        if not (subject and content):
            error = "Please enter both subject and content."
            self.render("newpost.html", error=error,
                        subject=subject, content=content)
        else:
            user = self.validate_user()
            # redirect to login if cookie wrong
            if not user:
                return self.redirect("/blog/login")
            # create BlogPost instance for current user
            blog = BlogPost(subject=subject, content=content, user=user)
            blog.put()  # insert into db
            id = blog.key().id()
            self.redirect("/blog/" + str(id))  # redirect to permalink
