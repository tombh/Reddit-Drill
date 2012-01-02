from google.appengine.ext import webapp
from app.model import Story
import json, zlib, base64

class getStory(webapp.RequestHandler):
  def get(self):
    id = self.request.get('id')
    story = Story().getById(id)
    result = json.dumps(False)
    if story:
      if story.compressed:
        result = zlib.decompress(base64.b64decode(story.json))
      else:
        result = story.json
    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(result)

