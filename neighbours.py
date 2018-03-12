# Download the neighbours (followers or followees) of a set of users
# Create an adjacency matrix and a similarity matrix
# Both matrices can be read by Gephi
# The similarity matrix is also plotted as a matrix in R

import yaml
import argparse
import tweepy
import os
import csv
import time
from tweepy import TweepError
from utils import fetch_neighbours, make_similarity_matrix, make_adjacency_matrix

with open('config_neighbours.yml', 'r') as f:
    doc = yaml.load(f)
    CONSUMER_KEY = doc["CONSUMER_KEY"]
    CONSUMER_SECRET = doc["CONSUMER_SECRET"]


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=60)

PATHS = {"in": "./followers/",
         "out": "./followees/",
         "names": "./screen_names/",
         "outputs": "./outputs/"}



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", required=True, help="A file with usernames")
    parser.add_argument("-d", "--direction", required=True, help="Followers or followees",
    	 				choices=['followers', 'followees'])
    parser.add_argument("-f", "--function", required=True, help="Function to execute", 
		choices=['fetch', 'make_similarity', 'make_adjacency'])

    args = vars(parser.parse_args())
    file = args['list']
    direction = args['direction']
    function = args['function']

    if (direction == 'followers'):
    	direction = 'in'
    if (direction == 'followees'):
    	direction = 'out'
	
	# Read the list of users
    users = []
    with open(file, 'r') as f:
    	csvreader = csv.reader(f, delimiter=' ')
    	for i, row in enumerate(csvreader):
    		users.append(row[0])

    while(True): 
        try:
        	if(function == 'fetch'):
        		# Get neighbours of each user in the list
        		for i, user in enumerate(users):
        			print(i, user)
        			userid = api.get_user(user).id
        			fetch_neighbours(userid, api, direction=direction)
        			# Save the id-screen_name pair since we have it already
        			with open(os.path.join('screen_names', str(userid)), 'w') as f:
        				f.write(user)

	        if(function == 'make_similarity'):
	        	print("Creating similarity matrix")
	        	fout = 'similarity' + '_' + file.split('.')[0] + '_' + direction + '.csv'
	        	make_similarity_matrix(users, direction = direction, file = fout)

	        if(function == 'make_adjacency'):
	        	print("Creating adjacency matrix")
	        	fout = 'adjacency' + '-' + file.split('.')[0] + '_' + direction + '.csv'
	        	make_adjacency_matrix(users, direction = direction)
        	
        	break

        except TweepError as e:
            print(e)
            time.sleep(60)