# Download the neighbours of a keyword participants
# Create an adjacency matrix
# Both matrices can be read by Gephi

import argparse
import os
import csv
import tweepy
import datetime
import numpy as np
import yaml
import json
from tweepy import TweepError
from matplotlib import pylab as plt
from collections import Counter


with open('config_keywords.yml', 'r') as f:
    doc = yaml.load(f)
    CONSUMER_KEY = doc["CONSUMER_KEY"]
    CONSUMER_SECRET = doc["CONSUMER_SECRET"]
    ACCESS_TOKEN = doc["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = doc["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
#auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_errors=88, retry_delay=60)


path = './followers/'
if not os.path.exists(path):
    os.makedirs(path)

path = './outputs/'
if not os.path.exists(path):
    os.makedirs(path)

path = './screen_names/'
if not os.path.exists(path):
    os.makedirs(path)

PATHS = {"in": "./followers/",
         "out": "./followees/",
         "names": "./screen_names/",
         "outputs": "./outputs/"}

def api_neighbours_ids(user, direction="in"):
    if direction == "in":
        neighbours_ids = api.followers_ids(user)

    else:
        neighbours_ids = api.friends_ids(user)

    return neighbours_ids

def fetch_neighbours(userid, direction="in"):
    fname = os.path.join(PATHS[direction], str(userid))

    # If user is already tracked, get their followers from file
    if os.path.isfile(fname):
        print("User had already been fetched\n")

    # otherwise use the API
    else:
        try:
            # https://dev.twitter.com/rest/reference/get/followers/ids
            # 15 calls / 15 mins
            with open(fname, 'w') as f:
                neighbours = api_neighbours_ids(userid, direction)                
                csv.writer(f).writerow(neighbours)
        except TweepError as e:
            print(e)
            if e == "Not authorized.":
                writer.writerow("")

def get_participants(keyword):
    participants = {}
    with open('tracked/' + keyword + ".json", 'r') as f:    
        data = json.load(f)
        for entry in data:
            if entry["user_id"] not in participants:
                participants[entry["user_id"]] = entry['user'] 

    return participants

def get_locations(keyword):
    locations = []
    with open('tracked/' + keyword + ".json", 'r') as f:    
        data = json.load(f)
        for entry in data:
            locations.append(entry['user_location'])       

    return locations
 
    
def api_participans_neighbours(keyword):
    """ Get the neighbourhood of the N top participans"""
    participants = get_participants(keyword).keys()
    pids = participants.keys()
    pids= set([pid for pid, count in Counter(pids).most_common(500)])

    for i, pid in enumerate(participants):
        print("Processed:" + str(i) + "/" + str(len(participants)))
        print("User: ", str(pid))
        fetch_neighbours(pid)

        with open(os.path.join('screen_names', str(pid)), 'w') as f:
            f.write(participants[uid])


#################################################
# Create edge list using the followers directory
# where we downloaded the list of followers ids 
# of every user
#################################################
def build_graph(keyword):

    participants = get_participants(keyword)
    participants_ids = participants.keys()

    # Only consider participants for whom we know
    # the list of followers
    tracked_participants = []
    for uid in participants_ids:
        fname = os.path.join("followers", str(uid))
        if os.path.isfile(fname):
            tracked_participants.append(uid)

    # Create a list of edges 
    # and a list of vertices       
    edges = []
    vertices = []
    for i, uid in enumerate(tracked_participants):
        print(i)
        fname = os.path.join("followers", str(uid))
        
        # insert it in the list of vertices
        vertices.append((participants[uid], uid))
        
        # create its edges
        with open(fname, 'r') as f:
            print("user", participants[uid])
            line = f.readline()
            followers = line.split(',')
            if followers[0] == '':
                continue
            print(len(followers))
            count = 0 # number of followers that participated in the hashtag
            for fid in followers:
                try:
                    fid = int(fid)
                except ValueError as e:
                    print(e)
                    break
                if fid in tracked_participants:
                    count += 1
                    edges.append((participants[fid], participants[uid]))
            print(count)


    # Copy to files
    fname = os.path.join(PATHS["outputs"], 'edges.csv')
    with open(fname, 'w') as f:
        writer = csv.writer(f)
        for e in edges:
            writer.writerow(e)
        f.close()
        
    fname = os.path.join(PATHS["outputs"], 'vertices.csv')
    with open(fname, 'w') as f:
        writer = csv.writer(f)
        for v in vertices:
            writer.writerow(v)
        f.close()

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keyword", required=True, help="A tracked keyword")
    parser.add_argument("-f", "--function", required=True, help="Function to execute",
                        choices=['api_neighbours', 'api_names', 'api_graph'])
    
    args = vars(parser.parse_args())
    keyword = args['keyword']
    function = args['function']

    while(True): 
        try:
            if function == 'api_neighbours':
                api_participans_neighbours(keyword)
                build_graph(keyword)

            if function == 'api_graph': 
                build_graph(keyword)
            
            break
        except TweepError as e:
            print(e)
            time.sleep(60)