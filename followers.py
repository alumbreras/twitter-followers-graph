# Get egonet of a user and write it into a Gephi file
# The egonet is made of all its followers and the edges between followers
# author: Alberto Lumbreras
###########################################################################
import argparse
import csv
import os
import time
import tweepy
import yaml
from tweepy import TweepError
from xml.sax.saxutils import escape

# Read keys from file that contains
# CONSUMER_KEY: 6it3IkPFI4RNIGhIci1w
# CONSUMER_SECRET: zGUE1bTucHcNn5IxFNyBP8dN2EvbrMtij5xuWHqcW0
with open('config.yml', 'r') as f:
    doc = yaml.load(f)
    CONSUMER_KEY = doc["CONSUMER_KEY"]
    CONSUMER_SECRET = doc["CONSUMER_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

path = './followers/'
if not os.path.exists(path):
    os.makedirs(path)

path = './outputs/'
if not os.path.exists(path):
    os.makedirs(path)

path = './screen_names/'
if not os.path.exists(path):
    os.makedirs(path)
    
def api_followers(ego_screenname):
    """ Get the followers of ego and the followers of its followers
        Store everyting in files
    """
    # ego id
    ego = api.get_user(ego_screenname).id

    # Ego followers ids
    ego_followers = api.followers_ids(ego)
    with open(os.path.join('followers', str(ego)), 'w') as f:
        csv.writer(f).writerow(ego_followers)
    
    print "Ego followers:", len(ego_followers)
    # Followers ids of ego followers
    # sleep for a while when we reach the API limit
    while(True):
        for u in ego_followers:
            print "User: " + str(u)
            fname = os.path.join("followers", str(u))
    
            # If user is already tracked, get their followers from file
            if os.path.isfile(fname):
                with open(fname, 'r') as f:
                    print str(u) + " had already been fetched\n"
    
            # otherwise use the API
            else:
                print(u)
                try:
                    # https://dev.twitter.com/rest/reference/get/followers/ids
                    # 15 calls / 15 mins
                    with open(fname, 'w') as f:                
                        csv.writer(f).writerow(api.followers_ids(u))
                except TweepError as e:
                    print e
                    time.sleep(60)
        break


def api_followers_screen_names(ego_screenname):
    """Get the screen name of every ego follower"""
    ego = api.get_user(ego_screenname).id
    print "Getting screen names for followers of", ego_screenname
        
    # Read followers from file
    fname = os.path.join("followers", str(ego))
    if not os.path.isfile(fname):
        print "User not tracked yet"
        return
    
    with open(fname, 'r') as f:
        followers = [int(id) for line in csv.reader(f) for id in line]
    
    # Get screen_name of each follower and store in into a file    
    users = followers + [ego]
    n_users = len(users)
    batch_start = 0
    batch_end = min(100, n_users)
    while(batch_start < n_users):
        try:
            users_batch = api.lookup_users(followers[batch_start:batch_end])
            for u in users_batch:
                print u.screen_name
                with open(os.path.join('screen_names', str(u.id)), 'w') as f:
                    f.write(u.screen_name)
        except TweepError as e:
            print e
            time.sleep(60)
            
        batch_start += 100
        batch_end = min(batch_end+100, n_users) 

    print "Number of followers:", n_users - 1

def graph(ego_screenname):
    """Build the a graph of the egonet of ego"""
    ego = api.get_user(ego_screenname).id
    
    all_followers = {}
    screen_names = {}

    # Read ego_followers from file    
    with open(os.path.join('followers', str(ego)), 'r') as f:
        ego_followers = [int(id) for line in csv.reader(f) for id in line]

    # A dictionary to store ego followers and followers of followers
    # We can already fill it with the ego followers
    all_followers = {}
    all_followers[ego] = ego_followers
    
    # A dictionaty that will map ids to screen_names
    # we can already fill it with the ego screen_name
    screen_names = {}
    screen_names[ego] = ego_screenname
    
    # Fill both dictionaries with information stored in files
    for u in all_followers[ego]:
        fname = os.path.join('followers', str(u))
        try:
            with open(fname, 'r') as f:
                all_followers[u] = [int(id) for line in csv.reader(f) for id in line]
        except IOError:
            pass # followers of this user not yet fetched
            
        fname = os.path.join('screen_names', str(u))
        try:
            with open(fname, 'r') as f:        
                screen_names[u] = f.read()
        except IOError:
            pass # screen name of this user not yet fetched
            
    # Create graphML
    print "Writing graph..."
    path = './outputs/'
    if not os.path.exists(path):
        os.makedirs(path)
    
    with open(path + ego_screenname + '.graphml', 'w') as out:
        # header
        out.write("""<?xml version="1.0" encoding="UTF-8"?>
        <graphml xmlns="http://graphml.graphdrawing.org/xmlns"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
        http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
        \n""")
        
        # General specifications
        out.write("""<key id="name" for="node" attr.name="name" attr.type="string" />\n""")
        out.write("""<graph edgedefault="directed">\n\n""")
    
        # Add nodes (ego plus one node for each follower)
        # if we don't have its screen_name, use its user id as name
        out.write("<node id='%d'><data key='name'>%s</data></node>\n" % (ego, escape(screen_names[ego])))
        for f_id in all_followers[ego]:
                if screen_names.has_key(f_id):
                    screen_name =  escape(screen_names[f_id])
                else:
                    screen_name =  f_id                
                out.write("<node id='%d'><data key='name'>%s</data></node>\n" % (f_id, screen_name))
         
        edge_id = 0
        
        neighbourhood = all_followers[ego]
        neighbourhood.append(ego)
        
        # Add edges to ego and between ego followers
        for f_id, ff_ids in all_followers.iteritems():
            for ff_id in set(ff_ids).intersection(neighbourhood):
                out.write("<edge id='edge%d' source='%d' target='%d' />\n" % (edge_id, ff_id, f_id))
                edge_id += 1
        
        # Close graphml object
        out.write("</graph></graphml>")

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--screen_name", required=True, help="Screen name of twitter user")
    parser.add_argument("-f", "--function", required=True, help="Function to execute",
                        choices=['api_followers', 'api_screen_name', 'graph'])
    
    args = vars(parser.parse_args())
    screen_name = args['screen_name']
    function = args['function']    
    
    if function == 'api_followers':
        api_followers(screen_name)
        
    if function == 'api_screen_name': 
        api_followers_screen_names(ego_screenname=screen_name)

    if function == 'graph':    
        graph(screen_name)