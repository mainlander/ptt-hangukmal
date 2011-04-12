# -*- coding: utf-8 -*-

import os.path
import hashlib
import time

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users

class Meet13Record(db.Model):
    name = db.StringProperty()
    ptt_id = db.StringProperty()
    sex = db.StringProperty()
    phone = db.PhoneNumberProperty()
    email = db.StringProperty()
    msn = db.StringProperty()
    person_count = db.IntegerProperty()
    level = db.IntegerProperty()
    motive = db.StringProperty()
    location = db.StringProperty()
    transport = db.StringProperty()
    suggest = db.TextProperty()
    other = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    record_hash = db.StringProperty()
    korea_inst = db.BooleanProperty()
    korean_inst_name = db.StringProperty()
    korean_inst_level = db.StringProperty()
    learn_hour = db.IntegerProperty()
    begin_time = db.IntegerProperty()
    

class Meet13ApplyPage(webapp.RequestHandler):
    def get(self):
        size = 0
        items = Meet13Record.all()
        for item in items:
            size += item.person_count
        template_values = {
                            "size": size
                          }
        path = os.path.join(os.path.dirname(__file__), "meet13", "apply.html")
        self.response.out.write(template.render(path, template_values))

class Meet13Add(webapp.RequestHandler):
    def post(self):
        item = Meet13Record()
        item.ptt_id = self.request.get("pttid")
        item.name = self.request.get("name")
        item.sex = self.request.get("sex")
        item.phone = self.request.get("phone")
        item.email = self.request.get("email")
        item.msn = self.request.get("msn")
        item.person_count = int(self.request.get("people"))
        item.level = int(self.request.get("level"))
        item.motive = self.request.get("motive")
        item.location = self.request.get("location")
        item.transport = self.request.get("transport")
        item.suggest = self.request.get("suggest")
        item.other = self.request.get("other")
        item.korea_inst = True if self.request.get("korea_learn") == "1" else False
        item.korean_inst_name = self.request.get("inst_name")
        item.korean_inst_level = self.request.get("inst_level")
        item.learn_hour = int(self.request.get("thour"))
        item.begin_time = int(self.request.get("btime"))

        m = hashlib.md5()
        m.update(item.ptt_id)
        m.update(item.phone)
        m.update(time.strftime("%Y-%m-%d %H:%M:%S"))
        record_hash = m.hexdigest()
        item.record_hash = "m13-" + record_hash

        item.put()

        level_str = u"完全不會"
        if item.level == 1:
            level_str = u"初學"
        elif item.level == 2:
            level_str = u"中級"
        elif item.level == 3:
            level_str = u"高級"
        elif item.level == 4:
            level_str = u"母語"

        template_values = {
                            "item": item,
                            "level_str": level_str
                          }
        path = os.path.join(os.path.dirname(__file__), "meet13", "confirm.html")
        self.response.out.write(template.render(path, template_values))

class Meet13ConfirmPage(webapp.RequestHandler):
    def get(self):
        record_hash = self.request.get("ident")
        items = Meet13Record.all().filter("record_hash = ", record_hash)
        template_values = {}
        for item in items:
            template_values["item"] = item
            level_str = u"完全不會"
            if item.level == 1:
                level_str = u"初學"
            elif item.level == 2:
                level_str = u"中級"
            elif item.level == 3:
                level_str = u"高級"
            elif item.level == 4:
                level_str = u"母語"
            template_values["level_str"] = level_str
        path = os.path.join(os.path.dirname(__file__), "meet13", "confirm.html")
        self.response.out.write(template.render(path, template_values))


class Meet13ListPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                size = 0
                items = Meet13Record.all()
                level_list = [ 0, 0, 0, 0, 0 ]
                btime_list = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                korea_list = [ 0, 0 ]
                for item in items:
                    level_list[item.level] += 1
                    btime_list[item.begin_time] += 1
                    size += item.person_count
                    if item.korea_inst:
                        korea_list[0] += 1
                    else:
                        korea_list[1] += 1
                level_chart_str = "%d,%d,%d,%d,%d" % tuple(level_list)
                level_chart_max = "%d" % max(level_list)
                btime_chart_str = "%d,%d,%d,%d,%d,%d,%d,%d,%d" % tuple(btime_list)
                btime_chart_max = "%d" % max(btime_list)
                korea_inst_value = "%d,%d" % tuple(korea_list)
                template_values = {
                                    "items": items,
                                    "size": size,
                                    "level_chart_max": level_chart_max,
                                    "level_chart_value": level_chart_str,
                                    "btime_chart_max": btime_chart_max,
                                    "btime_chart_value": btime_chart_str,
                                    "korea_inst_value": korea_inst_value
                                  }
                path = os.path.join(os.path.dirname(__file__), "meet13", "list.html")
                self.response.out.write(template.render(path, template_values))
            else:
                self.response.out.write("<html><body>You are not allowed to see it. Please login your GMail account as Administrator.</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))
