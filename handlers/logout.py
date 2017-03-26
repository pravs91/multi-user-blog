from handler import Handler


class LogoutHandler(Handler):

    # delete cookie and redirect to /login
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user=; Path=/')
        self.redirect("/blog/login")
