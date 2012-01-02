from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from app.model import Story
import os

TEMPLATE_DIR = path = os.path.join(os.path.dirname(__file__), 'templates/')

class frontPage(webapp.RequestHandler):
  def get(self):
    stories = Story.all().filter('status = ', 'archived').order('-comments')
    self.response.out.write(template.render(TEMPLATE_DIR + 'index.html', {'stories' : stories, 'page': 'index'}))

class storyViewer(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render(TEMPLATE_DIR + 'viewer.html', {'page': 'viewer'}))
