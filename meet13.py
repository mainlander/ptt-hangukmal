# -*- coding: utf-8 -*-

import os.path
import hashlib
import time

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

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
    

class Meet13ApplyPage(webapp.RequestHandler):
    def get(self):
        size = Meet13Record.all().count()
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



class Meet13ListPage(webapp.RequestHandler):
    def get(self):
        items = Meet13Record.all()
        template_values = {
                            "items": items
                          }
        path = os.path.join(os.path.dirname(__file__), "meet13", "list.html")
        self.response.out.write(template.render(path, template_values))
