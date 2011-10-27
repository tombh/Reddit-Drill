############################################################################################
#This is the original Reddit Drill.
#It produces an HTML list of the the top reply to each comment, as far as it can drill down.
############################################################################################

from pprint import pprint
import sys
import urllib
import json

def get_permalink(comment_id = ''):
    return "http://www.reddit.com/r/AskReddit/comments/ks4da/we_had_to_temporarily_block_the_what" + "/" + comment_id

def get_data(comment_id = ''):
    submission = get_permalink(comment_id)
    url = submission + ".json?sort=top"
    print(url)
    return json.loads(urllib.urlopen(url).read())

#pprint(story[1]['data']['children'][0]['data']['body'])
#sys.exit()

story = get_data()
comments = story[1]['data']['children']
top_reply = comments[0]['data']

f = open('/var/www/tombh/reddit_drill/drill.html', 'w')
f.write('<ul>' + "\n")

count = 0
while True:
    count += 1
    string = str(count) + ": " + top_reply['body']
    pprint(string)
    line = ('<li>' + string + ' <a href="' + get_permalink(top_reply['id']) + '">permalink</a></li>' + "\n").encode('UTF-8')
    f.write(line)
    parent = top_reply
    top_reply = top_reply['replies']['data']['children'][0]['data']
    if 'body' not in top_reply:
        comment_id = parent['id']
        result = get_data(comment_id)
        top_reply = result[1]['data']['children'][0]['data']['replies']['data']['children'][0]['data']


f.write('</ul>' + "\n")
