#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from meet13 import *
from meet14 import *
from meet15 import *

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hello world!')


def main():
    application = webapp.WSGIApplication([
            ('/', MainHandler), 
            ('/meet13/apply', Meet13ApplyPage),
            ('/meet13/add', Meet13Add),
            ('/meet13/list', Meet13ListPage),
            ('/meet13/confirm', Meet13ConfirmPage),
            ('/meet13/sugcom', Meet13SugcomPage),
            ('/meet14/apply', Meet14ApplyPage),
            ('/meet14/add', Meet14Add),
            ('/meet14/list', Meet14ListPage),
            ('/meet14/confirm', Meet14ConfirmPage),
            ('/meet14/sugcom', Meet14SugcomPage),
            ('/meet15/apply', Meet15ApplyPage),
            ('/meet15/add', Meet15Add),
            ('/meet15/list', Meet15ListPage),
            ('/meet15/confirm', Meet15ConfirmPage),
            ('/meet15/sugcom', Meet15SugcomPage)
                                         ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
