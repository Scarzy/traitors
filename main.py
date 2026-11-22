#!/usr/bin/env python3

import yaml
import asyncio
import tornado
import mysql.connector as mysql

def load_mysql_creds():
    with open("creds.yaml") as stream:
        try:
            data = yaml.safe_load(stream)
            user = data["user"]
            password = data["password"]
        except:
            print("Whoops...")
    return user,password

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
        (r"/manage", UserPageHandler),
        (r"/users", UsersHandler),
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
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT name,score FROM christmasawake2026")
        res = cursor.fetchall()
        print(res)
        self.write('[{"name":"steve", "score":55555},{"name":"stew", "score":4444},{"name":"stevie", "score":333},{"name":"stephen", "score":22},{"name":"steven", "score":1}]')

class ScoreboardHandler(BaseHandler):
    def get(self):
        self.render("static/html/scoreboard.html")

class UsersHandler(BaseHandler):
    def get(self):
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT name,role FROM christmasawake2026")
        res = cursor.fetchall()
        print(res)
        self.write('[{"name":"steve", "score":55555},{"name":"stew", "score":4444},{"name":"stevie", "score":333},{"name":"stephen", "score":22},{"name":"steven", "score":1}]')

class UserPageHandler(BaseHandler):
    def get(self):
        self.render("static/html/users.html")


async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
