from handler import Handler


class MainPage(Handler):

    def get(self):
        self.redirect('/blog')
