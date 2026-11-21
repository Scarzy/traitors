#!/usr/bin/env python3

import asyncio
import tornado

def make_app():
    settings = {
            "login_url": "/login",
            "cookie_secret": "dFizkvPwQQsZeM2twrYIo96IGFBytn9Mm0QHv7WizULfCE43JVEf0HZpSADkSq0rjMaaThQbpBWY3oRmy9OQLg=="
            }
    return tornado.web.Application([
        (r"/", ScoreboardHandler),
        (r"/login", LoginHandler),
        (r"/scorer", ScorerHandler),
        (r"/scoreboard", ScoreboardHandler),
        (r"/scores", ScoresHandler),
        (r'/(.*\..*)', tornado.web.StaticFileHandler, {'path': "static"}),
        ],
        **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_signed_cookie("user")

class IndexHandler(BaseHandler):
    def get(self):
        self.render("static/html/index.html")

class LoginHandler(BaseHandler):
    def get(self, creds=None):
        self.render("static/html/login.html")
    
    def post(self):
        self.set_signed_cookie("user",self.get_argument("name"))
        self.redirect("/")

class ScorerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("static/html/index.html")

class ScoresHandler(BaseHandler):
    def get(self):
        self.write('[{"name":"steve", "score":55555},{"name":"stew", "score":4444},{"name":"stevie", "score":333},{"name":"stephen", "score":22},{"name":"steven", "score":1}]')

class ScoreboardHandler(BaseHandler):
    def get(self):
        self.render("static/html/scoreboard.html")


async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
