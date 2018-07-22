"""Models used in this application"""

from google.appengine.ext import db

class Poll(db.Model):
    name = db.StringProperty(required = True)  
    values = db.StringListProperty(required = True)

class ActivePoll(db.Model):
    """For storing the active poll. We will use only one register"""
    mkey = db.StringProperty(required = True)  #we are going to use "activepoll"
    poll = db.ReferenceProperty(Poll)

class Vote(db.Model): #Assumed one vote per user
    poll = db.ReferenceProperty(Poll, required = True)
    user = db.UserProperty(required = True)
    value = db.StringProperty() 


