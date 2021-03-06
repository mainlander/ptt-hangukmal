# -*- coding: utf-8 -*-

import os.path
import hashlib
import time

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users

class Meet14Record(db.Model):
    name = db.StringProperty()
    ptt_id = db.StringProperty()
    sex = db.StringProperty()
    phone = db.PhoneNumberProperty()
    email = db.StringProperty()
    msn = db.StringProperty()
    person_count = db.IntegerProperty()
    level = db.IntegerProperty()
    motive = db.StringListProperty()
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
    

class Meet14ApplyPage(webapp.RequestHandler):
    def get(self):
        size = 0
        items = Meet14Record.all()
        for item in items:
            size += item.person_count
        template_values = {
                            "size": size
                          }
        path = os.path.join(os.path.dirname(__file__), "meet14", "apply.html")
        self.response.out.write(template.render(path, template_values))

class Meet14Add(webapp.RequestHandler):
    def post(self):
        item = Meet14Record()
        item.ptt_id = self.request.get("pttid")
        item.name = self.request.get("name")
        item.sex = self.request.get("sex")
        item.phone = self.request.get("phone")
        item.email = self.request.get("email")
        item.msn = self.request.get("msn")
        item.person_count = int(self.request.get("people"))
        item.level = int(self.request.get("level"))
        item.motive = self.request.get("motive", allow_multiple=True)
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
        item.record_hash = "m14-" + record_hash

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

#        template_values = {
#                            "item": item,
#                            "level_str": level_str
#                          }
        self.redirect("/meet14/confirm?ident=" + item.record_hash)
#        path = os.path.join(os.path.dirname(__file__), "meet14", "confirm.html")
#        self.response.out.write(template.render(path, template_values))

class Meet14ConfirmPage(webapp.RequestHandler):
    def get(self):
        record_hash = self.request.get("ident")
        items = Meet14Record.all().filter("record_hash = ", record_hash)
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
        path = os.path.join(os.path.dirname(__file__), "meet14", "confirm.html")
        self.response.out.write(template.render(path, template_values))


class Meet14ListPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                size = 0
                items = Meet14Record.all()
                level_list = [ 0, 0, 0, 0, 0 ]
                btime_list = [ 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
                korea_list = [ 0, 0 ]
                thour_list = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
                for item in items:
                    level_list[item.level] += 1
                    btime_list[item.begin_time] += 1
                    size += item.person_count
                    if item.korea_inst:
                        korea_list[0] += 1
                    else:
                        korea_list[1] += 1
                        thour_list[item.learn_hour] += 1
                level_chart_str = "%d,%d,%d,%d,%d" % tuple(level_list)
                level_chart_max = "%d" % max(level_list)
                btime_chart_str = "%d,%d,%d,%d,%d,%d,%d,%d,%d" % tuple(btime_list)
                btime_chart_max = "%d" % max(btime_list)
                korea_inst_value = "%d,%d" % tuple(korea_list)
                thour_chart_str = "%d,%d,%d,%d,%d,%d,%d,%d" % tuple(thour_list)
                thour_chart_max = "%d" % max(thour_list)
                template_values = {
                                    "items": items,
                                    "size": size,
                                    "level_chart_max": level_chart_max,
                                    "level_chart_value": level_chart_str,
                                    "btime_chart_max": btime_chart_max,
                                    "btime_chart_value": btime_chart_str,
                                    "korea_inst_value": korea_inst_value,
                                    "thour_chart_max": thour_chart_max,
                                    "thour_chart_value": thour_chart_str
                                  }
                path = os.path.join(os.path.dirname(__file__), "meet14", "list.html")
                self.response.out.write(template.render(path, template_values))
            else:
                self.response.out.write("<html><body>You are not allowed to see it. Please login your GMail account as Administrator.</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))

class Meet14SugcomPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        btime_names = [ u"無", u"一個月內", u"1～3個月", u"3～6個月", 
                        u"半年～一年", u"一～三年", u"三～五年", 
                        u"五～十年", u"十年以上" ]
        thour_names = [ u"0小時", u"100小時以內", u"100～200小時", 
                        u"200～300小時", u"300～400小時", u"400～500小時",
                        u"500～600小時", u"600小時以上" ]
        if user:
            if users.is_current_user_admin():
                record_hash = self.request.get("record")
                items = Meet14Record.all().filter("record_hash = ", record_hash)
                ptt_id = ""
                location = ""
                transport = ""
                motive = ""
                suggest = ""
                other = ""
                motive = ""
                btime = ""
                thour = ""
                korea_inst = ""
                inst_name = ""
                inst_level = ""
                for item in items:
                    ptt_id = item.ptt_id
                    location = item.location
                    transport = item.transport
                    sugget = item.suggest
                    other = item.other
                    motive = ",".join(item.motive)
                    btime = btime_names[item.begin_time]
                    if item.korea_inst:
                        korea_inst = u"是"
                        inst_name = item.korean_inst_name
                        inst_level = item.korean_inst_level
                    else:
                        korea_inst = u"否"
                        thour = thour_names[item.learn_hour]
                template_values = {
                            "ptt_id": ptt_id,
                            "location": location,
                            "transport": transport,
                            "suggest": suggest,
                            "other": other,
                            "motive": motive,
                            "korea_inst": korea_inst,
                            "inst_name": inst_name,
                            "inst_level": inst_level,
                            "btime": btime,
                            "thour": thour
                        }
                path = os.path.join(os.path.dirname(__file__), "meet14", "sugcom.html")
                self.response.out.write(template.render(path, template_values))

            else:
                self.response.out.write("<html><body>You are not allowed to see it. Please login your GMail account as Administrator.</body></html>")
        else:
            self.redirect(users.create_login_url(self.request.uri))
