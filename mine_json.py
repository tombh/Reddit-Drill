from pprint import pprint
import sys, os
import urllib
import json

def get_permalink(comment_id = ''):
    return "http://www.reddit.com/r/AskReddit/comments/ks4da/we_had_to_temporarily_block_the_what" + "/" + comment_id

def get_data(comment_id = ''):
    submission = get_permalink(comment_id)
    url = submission + ".json?sort=top"
    print(url)
    return json.loads(urllib.urlopen(url).read())

def verbose(seam, depth):
    string = str(depth) + "(" + str(seam['data']['rating']) + "): " + seam['data']['body']
    pprint(string)

def drill(seam, depth):
    """
    I'm going to try and be verbose as I can in the function, cos it's very tricky
    Basically we're both cleaning *and* drilling. The function itself only parses one level at a time.
    Subsequent levels are accessed by recursion.
    """
    
    #Each level is a dictionary
    cleaned = dict()        
    cleaned["data"] = dict()    
    
    depth += 1    
    #if depth > 150: return #how far down the rabbit-hole do you want to go?
    
    #loop over the dict's *keys*, body, id, children, etc
    #this is looping over the raw JSON structure returned by the API
    for k,v in seam.iteritems():
        
        #REPLIES
        if k == "replies":
            
            if 'data' in v: #this is the sig that tells if it's actually worth mining further
                
                cleaned["children"] = list()
                
                #loop over the list of children
                children = v['data']['children']                
                offspring = 0
                for child in children:
                    
                    #only drill the first few replies
                    offspring += 1                    
                    #if offspring == 3: break
                    
                    #only recurse if there are deeper replies
                    #the sig for that is the 'body' key
                    if 'body' in child['data']:                        
                            #push item onto the end of the list
                            new_seam = drill(child['data'], depth)
                            if new_seam:
                                new_seam['data']['rating'] = offspring                        
                                cleaned["children"].append(new_seam)
                                verbose(new_seam, depth)
                    else:
                        comment_id = child['data']['id']
                        result = get_data(comment_id)
                        
                        #the result[0] is the first 'header' item that refers to the main story
                        #result[1] actually contains the continuing replies
                        new_kids = result[1]['data']['children']
                        if len(new_kids) > 0:
                            kidspring = 0
                            for kid in new_kids:
                                kidspring += 1                                
                                new_seam = drill(kid['data'], depth)
                                if new_seam:
                                    new_seam['data']['rating'] = kidspring
                                    cleaned["children"].append(new_seam)
                                    verbose(new_seam, depth)               
                 
        #BODY                        
        elif k == 'body':
            cleaned['name'] = v[:15]
            cleaned['data']['body'] = v            
            
        #ID
        elif k == 'id':
            cleaned['id'] = v
            cleaned['data']['id'] = v
            
        #EVERYTHING ELSE
        else:
            cleaned['data'][k] = v
            
    return cleaned




###############################################################################
#Let's get this show on the road
story = get_data()
comments = story[1]['data']['children']
trunk = comments[0]['data']
tree = drill(trunk, 0)

#write out the results
pprint('writing...')
f = open(os.getcwd() + '/drill.json', 'w')
f.write('var json = ' + json.dumps(tree) + ';')

f_debug = open(os.getcwd() + '/drill.debug', 'w')
f_debug.write(json.dumps(tree)) #so that chrome's json extension pretty prints it. useful for debugging

pprint('fin')