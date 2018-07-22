""" Poll administration """

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db
import webapp2
from models import Poll, ActivePoll


class AddPoll(webapp2.RequestHandler):
    """Adds poll to database"""
    def post(self):
        import cgi
        pname = cgi.escape(self.request.get('pname'))
        plist = cgi.escape(self.request.get('fields'))
        poll = db.get(db.Key.from_path("Poll", pname))
        if poll:
            #Checks if exists
            self.response.out.write('<html><body>Poll:<pre>')
            self.response.out.write(cgi.escape(self.request.get('pname')))
            self.response.out.write('</pre> wasn\' added: already exists <hr/>back to <a href="/admin/">admin</a></body></html>')
            return

        if len(plist.split(',')) < 2:
            #Validates field list
            self.response.out.write('<html><body>Poll:<pre>')
            self.response.out.write(cgi.escape(self.request.get('pname')))
            self.response.out.write('</pre> wasn\' added: not enough options <hr/>back to <a href="/admin/">admin</a></body></html>')
            return

        poll = Poll(key_name = pname, name = pname, values = plist.split(','))
        poll.put()
        self.response.out.write('<html><body>Poll:<pre>')
        self.response.out.write(cgi.escape(self.request.get('pname')))
        self.response.out.write('</pre> added successfully <hr/>back to <a href="/admin/">admin</a></body></html>')

class SetPoll(webapp2.RequestHandler):
    """Sets current poll"""
    def post(self):
        import cgi
        pname = cgi.escape(self.request.get('pname'))
        poll = db.get(db.Key.from_path("Poll", pname))
        apoll = ActivePoll.get_or_insert("key", mkey = "activepoll")
        apoll.poll = poll
        apoll.put()
        self.response.out.write('<html><body>Poll:<pre>')
        self.response.out.write(pname)
        self.response.out.write('</pre> selected <hr/>back to <a href="/admin/">admin</a></body></html>')


class MainPage(webapp2.RequestHandler):
    """Main administration view"""
    def get(self):
        user = users.get_current_user()
        if user:
            if users.is_current_user_admin():
                template_values = {}
                polls = Poll.gql( "ORDER BY name DESC")
                template_values["polls"] = polls
                apoll = ActivePoll.get_or_insert("key", mkey = "activepoll")
                try:
                    currentpoll = apoll.poll.name 
                except AttributeError:
                    currentpoll = "" #unable to retrieve current poll
                template_values["currentpoll"] = currentpoll.strip()
                import os
                path = os.path.join(os.path.dirname(__file__), 'admin.html')
                self.response.out.write(template.render(path, template_values))
            else:
                self.abort(403)
        else:
            self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([ 
    ('/admin/', MainPage), 
    ('/admin/set/', SetPoll), 
    ('/admin/add/', AddPoll), 
    ], debug=True)
