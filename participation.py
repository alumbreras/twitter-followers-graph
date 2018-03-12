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
import utils

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


def build_graph(keyword):
    """
    Create edge list using the followers directory
    where we downloaded the list of followers ids 
    of every user
    """
    participants = get_participants(keyword)
    participants_ids = participants.keys()

    # Only consider participants for whom we know
    # the list of followers
    tracked_participants = []
    for uid in participants_ids:
        fname = os.path.join(PATHS['in'], str(uid))
        if os.path.isfile(fname):
            tracked_participants.append(uid)

    # Create a list of edges 
    edges = []
    for i, uid in enumerate(tracked_participants):
        print(i)
        fname = os.path.join(PATHS['in'], str(uid))
        
        with open(fname, 'r') as f:
            print("user", participants[uid])
            line = f.readline()
            followers = line.split(',')
            if followers[0] == '':
                continue

            # create and edge from each follower
            for fid in followers:
                try:
                    fid = int(fid)
                except ValueError as e:
                    print(e)
                    break
                if fid in tracked_participants:
                    edges.append((participants[fid], participants[uid]))


    # Save to file
    fname = os.path.join(PATHS["outputs"], os.path.join(PATHS['output'], 'edges' + keyword + '.csv'))
    with open(fname, 'w') as f:
        writer = csv.writer(f)
        for e in edges:
            writer.writerow(e)
        f.close()


def build_dataset_participations():
    """ Creates a dataset will all participations """

    def get_participants(keyword):
        participants = {}
        with open('tracked/' + keyword + ".json", 'r') as f:
            data = json.load(f)
            for entry in data:
                if entry["user_id"] not in participants:
                    participants[entry["user_id"]] = entry['user']

        return participants


    filenames = listdir(PATHS["tracked"])
    with open(os.path.join(PATHS['outputs'], 'participations.csv'), 'w') as fout:
        csvwriter = csv.writer(fout, delimiter=',')
        for i, f in enumerate(filenames):
            print(f)
            participants = get_participants(f[:-5])
            for p in participants.values():
                csvwriter.writerow([p, i, 1]) 


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keyword", required=False, help="A tracked keyword")
    parser.add_argument("-f", "--function", required=True, help="Function to execute",
                        choices=['api_neighbours', 'build_graph', 'build_dataset_participations'])
    
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

            if function == 'dataset_participations': 
                build_dataset_participations()
            
            break
        except TweepError as e:
            print(e)
            time.sleep(60)