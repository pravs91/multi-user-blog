from models import BlogPost, User
from handler import Handler
from google.appengine.ext import db


class EditPageHandler(Handler):
    """A class to edit a blog post."""

    def get(self, blog_id):
        # check if user is logged in
        user = self.validate_user()
        if not user:
            return self.redirect("/blog/login")

        # retrieve blog and show edit page by pre-populating fields
        blog = BlogPost.get_by_id(int(blog_id))
        if blog:
            self.render("edit_page.html", user=user,
                        subject=blog.subject, content=blog.content)
        # redirect to /blog if post not found
        else:
            self.error_404("The requested blog URL was not found.")

    def post(self, blog_id):
        subject = self.request.get("subject")
        content = self.request.get("content")

        # validate subject and content present
        if not (subject and content):
            error = "Please enter both subject and content."
            self.render("edit_page.html", error=error,
                        subject=subject, content=content)
        else:
            user = self.validate_user()
            # redirect to login if cookie wrong
            if not user:
                return self.redirect("/blog/login")

            # retrieve blog post from db and edit fields
            blog = BlogPost.get_by_id(int(blog_id))
            if blog:
                blog.subject = subject
                blog.content = content
                blog.put()
                self.redirect('/blog/' + blog_id)
            # 404 error if blog not found
            else:
                self.error_404("The requested blog URL was not found.")
