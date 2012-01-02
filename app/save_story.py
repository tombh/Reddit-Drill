from google.appengine.ext import webapp
from google.appengine.api import taskqueue
from app.mine_json import Miner
from app.model import Story
import json, zlib, base64

class saveStory(webapp.RequestHandler):
  def get(self):
    result = dict()
    id = self.request.get('id')
    story = Story().getById(id)
    if story is False:
      #Just take a little peek for sanity's sake
      miner = Miner('/comments/' + id)
      info = miner.get_info()
      if info:
        if info['data']['num_comments'] > 300:
          taskqueue.add(url='/worker/save_story?id=' + id, method='GET')
          story = Story()
          story.id = id
          story.status = 'queued'
          story.put()
          result['message'] = 'Story added to queue for archiving'
        else:
          result['message'] = "That story doesn't have over 300 comments"
      else:
        result['message'] = "That story doesn't seem to exist. What does existence even mean?"
    elif story.status is 'queued':
      result['message'] = 'Still in the queue to be archived'
    else:
      result['message'] = 'Story already archived'

    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(result))

class saveStoryWorker(webapp.RequestHandler):
  def get(self):
    id = self.request.get('id')
    miner = Miner('/comments/' + id)
    tree = miner.populate()
    story = Story().getById(id)
    story.status = 'archived'
    story.name = tree['data']['title']
    story.comments = tree['data']['num_comments']
    story.permalink = tree['data']['permalink']
    story.compressed = True
    story.json = base64.b64encode(zlib.compress(json.dumps(tree), 9))
    story.put()


