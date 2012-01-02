from google.appengine.ext import db

class Story(db.Model):
  id = db.StringProperty()
  status = db.StringProperty()
  comments = db.IntegerProperty()
  depth = db.IntegerProperty()
  added = db.DateTimeProperty(auto_now_add=True)
  name = db.TextProperty()
  permalink = db.TextProperty()
  compressed = db.BooleanProperty()
  json = db.TextProperty()

  def getById(self, id):
    stories = self.all()
    stories.filter('id = ', id)
    story = stories.fetch(1)
    if len(story) == 1:
      return story[0]
    else:
      return False
