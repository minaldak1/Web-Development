import os
import webapp2
import jinja2
import logging
from google.appengine.api import memcache
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Art(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RequestHandler):
    def write(self, *args, **kws):
        self.response.out.write(*args, **kws)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kws):
        self.write(self.render_str(template, **kws))


def top(update = False):
    key = 'top'
    arts = memcache.get(key)
    if arts is None or update:
        logging.error("DB QUERY")
        arts = db.GqlQuery("SELECT * from Art ORDER BY created DESC")
        memcache.set(key , arts)
    return arts

class MainPage(Handler):

    def render_front(self, title="", art="", error=""):
        arts = top()
        self.render("front.html", title=title, art=art, error=error, arts=arts)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title=title, art=art)
            a.put()
            top(True)
            self.redirect("/")
        else:
            error = "We need both title and art"
            self.render_front(title=title, art=art, error=error)

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
