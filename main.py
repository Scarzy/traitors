#!/usr/bin/env python3

import os
import uuid
import math
import json
import yaml
import random
import asyncio
import tornado
import datetime
import mysql.connector as mysql

def load_cookie_creds():
    with open("creds.yaml") as stream:
        try:
            data = yaml.safe_load(stream)
            cookie = data["cookiesecret"]
        except:
            print("Whoops...")
    return cookie

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
    cookiesecret = load_cookie_creds()
    settings = {
            "login_url": "/",
            "cookie_secret": cookiesecret,
            "template_path": os.path.join(os.path.dirname(__file__),"templates"),
            }
    return tornado.web.Application([
        (r"/(favicon\.ico)",tornado.web.StaticFileHandler,{"path": os.path.join(os.path.dirname(__file__),"static","images"), "default_filename": "favicon.ico"}),
        (r"/", ScoreboardHandler),
        (r"/login", LoginHandler),
        (r"/scorer", ScorerHandler),
        (r"/scoreboard", ScoreboardHandler),
        (r"/schedule", ScheduleHandler),
        (r"/scores", ScoresHandler),
        (r"/scores/([0-9]+)", ScoresHandler),
        (r"/scoring", ScoringHandler),
        (r"/manage", ManagePageHandler),
        (r"/user", UserPageHandler),
        (r"/users", UsersHandler),
        (r"/whoami", WhoAmIHandler),
        (r"/users/([0-9]+)", UsersHandler),
        (r"/action/([0-9]+)", ActionHandler),
        (r"/majoraction", MajorActionHandler),
        (r"/thresholds", ThresholdHandler),
        (r"/votingtime", VotingTimeHandler),
        (r"/banishpage", BanishPageHandler),
        (r"/banish", BanishHandler),
        (r"/murderpage", MurderPageHandler),
        (r"/murder", MurderHandler),
        (r"/rules", RulesHandler),
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

class PageHandler(tornado.web.RequestHandler):
    @property
    def is_traitor(self):
        user_cookie = self.get_signed_cookie("user")
        uuid_cookie = self.get_signed_cookie("uuid")
        if not user_cookie or not uuid_cookie:
            return False
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT name,uid FROM christmasawake2026 WHERE role='traitor' AND name='{0}' AND uid='{1}'".format(user_cookie.decode("utf-8"), uuid_cookie.decode("utf-8")))
        if len(cursor.fetchall()) == 1:
            return True
        return False

    @property
    def is_admin(self):
        user_cookie = self.get_signed_cookie("user")
        uuid_cookie = self.get_signed_cookie("uuid")
        if not user_cookie or not uuid_cookie:
            return False
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT name,uid FROM christmasawake2026 WHERE admin=TRUE AND name='{0}' AND uid='{1}'".format(user_cookie.decode("utf-8"), uuid_cookie.decode("utf-8")))
        if len(cursor.fetchall()) == 1:
            return True
        return False

    @property
    def is_logged_in(self):
        return self.get_signed_cookie("uuid") and self.get_signed_cookie("user")

    def get_template_namespace(self):
        namespace = super().get_template_namespace()
        namespace["is_traitor"] = self.is_traitor
        namespace["is_logged_in"] = self.is_logged_in
        namespace["is_admin"] = self.is_admin
        return namespace

class BaseHandler(PageHandler):
    def get_current_user(self):
        return self.is_logged_in

class AdminHandler(PageHandler):
    def get_current_user(self):
        if not self.is_logged_in:
            return False
        return self.is_admin

class TraitorHandler(PageHandler):
    def get_current_user(self):
        if not self.is_logged_in:
            return False
        return self.is_traitor

class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html")

class LoginHandler(BaseHandler):
    def get(self, creds=None):
        self.render("login.html")
    
    def post(self):
        uuid_str = str(uuid.uuid4())
        role = random.choices(["faithful","traitor"], weights=[86,14])[0] 
        if self.get_argument("not-traitor", default=None) == "not-traitor":
            role = "faithful"
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO christmasawake2026 (name,uid,role) VALUES ('{0}','{1}','{2}') ON DUPLICATE KEY UPDATE name = VALUES(name)".format(self.get_argument("name"),uuid_str, role))
        conn.commit()
        self.set_signed_cookie("user",self.get_argument("name"))
        self.set_signed_cookie("uuid",uuid_str)
        self.redirect("/user")

class ScorerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("static/html/index.html")

class ScoresHandler(ScorerHandler):
    def get(self):
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT id,name,score FROM christmasawake2026 ORDER BY score DESC")
        res = cursor.fetchall()
        keys = ["id", "name", "score"]
        data = [dict(zip(keys, row)) for row in res]
        self.write(json.dumps(data))

    @tornado.web.authenticated
    def patch(self, slug):
        score = tornado.escape.json_decode(self.request.body)["score"]
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("UPDATE christmasawake2026 SET score = score + {1} WHERE id={0}".format(slug,score))
        conn.commit()
        self.write("{}")
        return

class ScoreboardHandler(BaseHandler):
    def get(self):
        self.render("scoreboard.html")

class ScheduleHandler(BaseHandler):
    def get(self):
        self.render("schedule.html")

class UsersHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self):
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT id,name,role FROM christmasawake2026")
        res = cursor.fetchall()
        keys = ["id", "name", "role"]
        data = [dict(zip(keys, row)) for row in res]
        self.write(json.dumps(data))

    @tornado.web.authenticated
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
    @tornado.web.authenticated
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

class MajorActionHandler(AdminHandler):
    @tornado.web.authenticated
    def put(self):
        action = tornado.escape.json_decode(self.request.body)["action"]
        match(action):
            case "dayturnover":
                user,password = load_mysql_creds()
                conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
                cursor = conn.cursor()
                cursor.execute("SELECT id,role,name,score,murdercount,recruitcount,banishcount FROM christmasawake2026")
                res = cursor.fetchall()
                keys = ["id","role","name","score","murdercount","recruitcount","banishcount"]
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
                cursor.execute("UPDATE christmasawake2026 SET murdervotes = 1 WHERE role='traitor'")
                conn.commit()
                cursor.execute("UPDATE christmasawake2026 SET banishvotes = 1")
                conn.commit()
                self.write("{}")
            case _:
                self.set_status(400)
                self.write("Action unknown")

class ScoringHandler(ScorerHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("scoring.html")

class ManagePageHandler(AdminHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("manage.html")

class UserPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("user.html")

class BanishPageHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("banish.html")

class BanishHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("static/html/banish.html")

class MurderPageHandler(TraitorHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("murder.html")

class MurderHandler(TraitorHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("static/html/murder.html")

class RulesHandler(BaseHandler):
    def get(self):
        self.render("rules.html")

class ThresholdHandler(BaseHandler):
    def get(self):
        data = get_count_thresholds()
        self.write(json.dumps(data))

class VotingTimeHandler(BaseHandler):
    def is_voting_valid(self):
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT murdervotes,banishvotes FROM christmasawake2026 WHERE name='{0}' AND uid='{1}'".format(self.get_signed_cookie("user").decode("utf-8"),self.get_signed_cookie("uuid").decode("utf-8")))
        res = cursor.fetchall()
        if len(res) == 0:
            res = [(0, 0),]
        now = datetime.datetime.now().minute
        return now >= 55 and now < 60 and (res[0][0] > 0 or res[0][1] > 0)
    
    @tornado.web.authenticated
    def get(self):
        data = {"vote": self.is_voting_valid()}
        self.write(json.dumps(data))
    
    @tornado.web.authenticated
    def put(self):
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        action = tornado.escape.json_decode(self.request.body)["action"]
        targetname = tornado.escape.json_decode(self.request.body)["targetname"]
        targetuuid = tornado.escape.json_decode(self.request.body)["targetuuid"]
        match(action):
            case "murder":
                #Check I am allowed to murder
                #Check target exists
                #Add 1 to target murdercount
                # Same for banish
                cursor.execute("SELECT id,role,name,score,murdercount,recruitcount,banishcount FROM christmasawake2026")
                res = cursor.fetchall()
                keys = ["id","role","name","score","murdercount","recruitcount","banishcount"]
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
                cursor.execute("UPDATE christmasawake2026 SET murdervotes = 1 WHERE role='traitor'")
                conn.commit()
                cursor.execute("UPDATE christmasawake2026 SET banishvotes = 1")
                conn.commit()
                self.write("{}")
            case _:
                self.set_status(400)
                self.write("Action unknown")

class WhoAmIHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user,password = load_mysql_creds()
        conn = mysql.connect(host="localhost", user=user, password=password, database="scouts")
        cursor = conn.cursor()
        cursor.execute("SELECT name,score,role FROM christmasawake2026 WHERE name='{0}' AND uid='{1}'".format(self.get_signed_cookie("user").decode("utf-8"),self.get_signed_cookie("uuid").decode("utf-8")))
        res = cursor.fetchall()
        keys = ["name", "score", "role"]
        data = [dict(zip(keys, row)) for row in res]
        self.write(json.dumps(data))


async def main():
    app = make_app()
    app.listen(8888, address="127.0.0.1", xheaders=True, max_body_size=20*1024*1024)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
