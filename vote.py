""" Vote action for users """

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import memcache
import webapp2
from models import Poll, ActivePoll, Vote


class VotePoll(webapp2.RequestHandler):
    """Perform the vote action"""
    def post(self):
        import cgi
        user = users.get_current_user()
        if not user:
            self.abort(403)
        value = cgi.escape(self.request.get('value'))
        pname = cgi.escape(self.request.get('poll'))
        poll = db.get(db.Key.from_path("Poll", pname))
        vote = Vote.get_or_insert("key", user = user, poll = poll)
        vote.value = value
        vote.put()
        self.response.out.write('<html><body>Thanks for voting! Your vote has been registered<hr/>back to <a href="/">vote</a></body></html>')


class MainPage(webapp2.RequestHandler):
    """Main poll vote view"""
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.out.write(self.get_vote()) #get from memcache method
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def get_vote(self):
        """Try to get content from memcache, generates and saves it if not possible"""
        vote = memcache.get("vote")
        if vote is not None:
            return vote
        else:
            vote = self.render_vote()
            if not memcache.add("vote", vote, 10):
                logging.error("Memcache set failed.")
            return vote

    def render_vote(self):
        """generates main view content"""
        template_values = {}
        apoll = ActivePoll.get_or_insert("key", mkey = "activepoll")
        poll = apoll.poll
        try:
            template_values["name"] = poll.name
            template_values["values"] = poll.values
        except AttributeError:
            self.abort(500)
        import os
        path = os.path.join(os.path.dirname(__file__), 'vote.html')
        return template.render(path, template_values)

app = webapp2.WSGIApplication([ 
    ('/', MainPage), 
    ('/vote_poll/', VotePoll), 
    ], debug=True)
