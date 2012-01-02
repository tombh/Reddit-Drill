############################################################################################
#This is an advanced drill that attempts to create structured JSON for The JIT - thejit.org.
#The JIT creates nice visualisations :)
############################################################################################

from pprint import pprint
import sys, os, time
import urllib2
import json
from google.appengine.api import urlfetch
import HTMLParser
from reddit_api_proxy import reddit_proxy

#pprint(sys.getrecursionlimit())
sys.setrecursionlimit(1000000)
#pprint(sys.getrecursionlimit())
#sys.exit()

class Miner:

    maxDepth = 100000
    maxRating = 10

    def __init__(self, url):
        self.url = reddit_proxy.api + url
        self.htmlParse = HTMLParser.HTMLParser()

    def get_permalink(self, comment_id = ''):
        return self.url + "/" + comment_id

    def get_data(self, comment_id = ''):
        submission = self.get_permalink(comment_id)
        url = submission + ".json?sort=top"
        print(url)
        result = urlfetch.fetch(url, deadline = 10)
        return json.loads(result.content)

    def drill(self, seam, depth, rating):
        """
        I'm going to try and be as verbose as I can in the function, cos it's very tricky
        Basically we're both cleaning *and* drilling. The function itself only parses one level at a time.
        Subsequent levels are accessed by recursion.

        The JIT expects JSON formatted as follows;
        var json = {
            id: "someKindOfUniqueID",
            name: "This appears as the label for the node",
            children: [{
                id: "someKindOfUniqueID",
                name: "This appears as the label for the node",
                data: {
                    these: "",
                    keys: "",
                    can: "",
                    be: "",
                    anythingYouWant: ""
                },
                children: []
            }]
        }

        The JIT-ready JSON is kept in the cleaned[] dictionary here.
        """

        #Each level is a dictionary
        cleaned = dict()
        cleaned["data"] = dict()

        depth += 1
        if depth > self.maxDepth: return cleaned #how far down the rabbit-hole do you want to go?

        #loop over the dict's *keys*, body, id, children, etc
        #this is looping over the raw JSON structure returned by the API
        for k,v in seam.iteritems():

            #ID
            if k == 'id':
                cleaned['id'] = v
                cleaned['data']['id'] = v

            #BODY
            elif k == 'body':
                cleaned['name'] = v[:50]
                cleaned['data']['body'] = v
                string = str(depth) + "(" + str(rating) + "): " + v
                pprint(string)

            #BODY HTML
            elif k == 'body_html':
                #convert html enities to their original characters
                cleaned['data']['body_html'] = self.htmlParse.unescape(v)


            #REPLIES
            elif k == "replies":

                if 'data' in v: #this is the sig that tells if it's actually worth mining further

                    children = list()
                    cleaned["children"] = list()

                    if 'more' in v['data']['children'][0]['kind']:
                        #We need to load a new page from the paginator
                        #Concerning the use of seam['id'] and the horribly long result[1]['data']['children'][0]['data']['replies']['data']['children']
                        #It's to do with the way reddit nests it's pagination in the returned JSON
                        #The 'more' key would seem to contain the comment_id fragment for the next page, but that doesn't seem to work,
                        #instead, it's better to take the parent comments id and then pop off the first comment from the new page,
                        #thus the need for the horribly long dictionary reference.
                        comment_id = seam['id']
                        result = self.get_data(comment_id)

                        replies = result[1]['data']['children'][0]['data']['replies']
                        if 'data' in replies:
                            children = replies['data']['children']

                    else:
                        children = v['data']['children']

                    cleaned["children"] = self.loop_children(children, depth)

            #EVERYTHING ELSE
            else:
                cleaned['data'][k] = v


        return cleaned

    def loop_children(self, children, depth):
        """
        #loop over the list of children
        #This is vertical drilling
        """

        rating = 0 #this keeps track of horizontal replies to the _same_ comment, we only want to drill the top few

        ore= list()
        for child in children:

            #only drill the first few replies
            rating += 1
            if rating > self.maxRating: break

            #only recurse if there are deeper replies
            #the sig for that is the 'body' key
            if 'body' in child['data']:
                new_seam = child['data']

                seam = self.drill(new_seam, depth, rating) #horizontal drilling
                if 'id' in seam:
                    seam['data']['rating'] = rating
                    seam['data']['depth'] = depth
                    ore.append(seam)

        return ore

    def populate(self):
        tree = self.get_info()
        if tree is False: return False
        #This is the actual comment data
        tree['children'] = list()
        trunk = self.story[1]['data']['children']
        tree['children'] = self.loop_children(trunk, 0)

        return tree

    def get_info(self):
        #It's useful to store all the meta data about a story
        self.story = self.get_data()
        if len(self.story) != 2:
          return False
        info = self.story[0]['data']['children'][0]['data']
        self.url = reddit_proxy.api + info['permalink']
        tree = dict()
        tree['id'] = 'trunk'
        tree['data'] = info
        if info['selftext_html']:
          tree['data']['body_html'] = self.htmlParse.unescape(info['selftext_html'])
        else:
          tree['data']['body_html'] = info['url']
        tree['name'] = info['title']

        return tree

