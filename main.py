#!/usr/bin/env python3

import math
import json
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
        (r"/users/([0-9+])", UsersHandler),
        (r"/action/([0-9+])", ActionHandler),
        (r"/majoraction", MajorActionHandler),
        (r"/thresholds", ThresholdHandler),
        (r'/(.*\..*)', tornado.web.StaticFileHandler, {'path': "static"}),
        ],
        **settings)

def get_count_thresholds():
    user,password = load_mysql_creds()
    conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM christmasawake2026")
    res = cursor.fetchall()
    totalentries = len(res)
    
    user,password = load_mysql_creds()
    conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM christmasawake2026 WHERE role='traitor'")
    res = cursor.fetchall()
    traitorentries = len(res)
    
    murderthreshold = math.ceil(2/3 * traitorentries)
    recruitthreshold = math.ceil(2/3 * traitorentries)
    banishthreshold = math.ceil(1/3 * totalentries)

    return {"murderthreshold": murderthreshold, "recruitthreshold": recruitthreshold, "banishthreshold": banishthreshold}

def get_scores():
    return {"murder": -100,
            "banish": -100,
            }

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
        cursor.execute("SELECT name,score FROM christmasawake2026 ORDER BY score DESC")
        res = cursor.fetchall()
        keys = ["name", "score"]
        data = [dict(zip(keys, row)) for row in res]
        self.write(json.dumps(data))

class ScoreboardHandler(BaseHandler):
    def get(self):
        self.render("static/html/scoreboard.html")

class UsersHandler(BaseHandler):
    def get(self):
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT id,name,role FROM christmasawake2026")
        res = cursor.fetchall()
        keys = ["id", "name", "role"]
        data = [dict(zip(keys, row)) for row in res]
        self.write(json.dumps(data))

    def patch(self, slug):
        role = tornado.escape.json_decode(self.request.body)["role"]
        match(role):
            case "traitor":
                pass
            case "faithful":
                pass
            case _:
                self.set_status(400)
                self.write("Role unknown")
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("UPDATE christmasawake2026 SET role='{1}' WHERE id={0}".format(slug,role))
        conn.commit()
        self.write("{}")

class ActionHandler(BaseHandler):
    def patch(self, slug):
        action = tornado.escape.json_decode(self.request.body)["action"]
        column = "count"
        match(action):
            case "murder":
                column = action + column
                pass
            case "recruit":
                column = action + column
                pass
            case "banish":
                column = action + column
                pass
            case "score":
                score = tornado.escape.json_decode(self.request.body)["score"]
                user,password = load_mysql_creds()
                conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
                cursor = conn.cursor()
                cursor.execute("UPDATE christmasawake2026 SET score = score + {1} WHERE id={0}".format(slug,score))
                conn.commit()
                self.write("{}")
                return
            case _:
                self.set_status(400)
                self.write("Action unknown {}".format(action))
                return
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("UPDATE christmasawake2026 SET {1} = {1} + 1 WHERE id={0}".format(slug,column))
        conn.commit()
        self.write("{}")

class MajorActionHandler(BaseHandler):
    def put(self):
        action = tornado.escape.json_decode(self.request.body)["action"]
        match(action):
            case "dayturnover":
                user,password = load_mysql_creds()
                conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
                cursor = conn.cursor()
                cursor.execute("SELECT id,name,score,murdercount,recruitcount,banishcount FROM christmasawake2026")
                res = cursor.fetchall()
                keys = ["id","name","score","murdercount","recruitcount","banishcount"]
                data = [dict(zip(keys, row)) for row in res]
                thresholds = get_count_thresholds()
                scores = get_scores()
                for user in data:
                    if user["murdercount"] >= thresholds["murderthreshold"]:
                        cursor.execute("UPDATE christmasawake2026 SET score = score + {1} WHERE id={0}".format(user["id"],scores["murder"]))
                        conn.commit()
                    if user["banishcount"] >= thresholds["banishthreshold"]:
                        cursor.execute("UPDATE christmasawake2026 SET score = score + {1} WHERE id={0}".format(user["id"],scores["banish"]))
                        conn.commit()
                    if user["recruitcount"] >= thresholds["recruitthreshold"]:
                        cursor.execute("UPDATE christmasawake2026 SET role='traitor' WHERE id={0}".format(user["id"]))
                        conn.commit()
                    cursor.execute("UPDATE christmasawake2026 SET murdercount=0,banishcount=0,recruitcount=0 WHERE id={0}".format(user["id"]))
                    conn.commit()
                self.write("{}")
            case _:
                self.set_status(400)
                self.write("Action unknown")

class UserPageHandler(BaseHandler):
    def get(self):
        self.render("static/html/users.html")

class ThresholdHandler(BaseHandler):
    def get(self):
        data = get_count_thresholds()
        self.write(json.dumps(data))


async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
