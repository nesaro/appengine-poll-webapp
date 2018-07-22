""" Poll results """

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import webapp2
from models import Poll, ActivePoll, Vote


class MainPage(webapp2.RequestHandler):
    """Main poll results view"""
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                template_values = {}
                pid = self.request.get('pid')
                if pid:
                    #try to get poll from GET parammeters
                    poll = db.get(db.Key.from_path("Poll", pid))
                else:
                    #default: active poll
                    apoll = ActivePoll.get_or_insert("key", mkey = "activepoll")
                    poll = apoll.poll
                try:
                    template_values["name"] = poll.name
                    template_values["values"] = poll.values
                except AttributeError:
                    self.abort(500)

                template_values["results"] = {}
                for value in template_values["values"]:
                    query = db.GqlQuery("SELECT * FROM Vote WHERE value = :1", value)
                    template_values["results"][value] = query.count(limit = None)
                #Alternative implementation: one query and iterate over results. I think it would be slower and harder to paralellize
                import os
                path = os.path.join(os.path.dirname(__file__), 'results.html')
                self.response.out.write(template.render(path, template_values))
            else:
                self.abort(403)
        else:
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([ 
    ('/results/', MainPage), 
    ], debug=True)
