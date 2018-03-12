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

def api_neighbours_ids(user, direction="in"):
    if direction == "in":
        neighbours_ids = api.followers_ids(user)

    else:
        neighbours_ids = api.friends_ids(user)

    return neighbours_ids


def fetch_neighbours(userid, direction = "in"):
	fname = os.path.join(PATHS[direction], str(userid))
	
	# If user is already tracked, get their followers from file
	if os.path.isfile(fname):
		print("User had already been fetched\n")

	# otherwise use the API
	else:
		try:
			with open(fname, 'w') as f:
				neighbours = api_neighbours_ids(userid, direction)
				csv.writer(f).writerow(neighbours)
		except TweepError as e:
			print(e)
			if e == "Not authorized.":
				writer.writerow("")

def make_similarity_matrix(users, file = "similarities.csv"):


	# Dictionary of usernames - id
	usernames = {}
	for uid in os.listdir(PATHS["names"]):
		fname = os.path.join(PATHS["names"], uid)
		with open(fname, 'r') as f:
			uname = f.readline()
			if uname in users:
				usernames[uid]  = uname

	print(users)

	# Create a dictionary with neighbours of each user
	neighbours = {}
	for uid in usernames:
		fname = os.path.join(PATHS["out"], uid)
		with open(fname, 'r') as f:
			n_neighbours = set([int(id) for line in csv.reader(f) for id in line])
			if(len(n_neighbours)>1000):
				neighbours[uid] = n_neighbours

	# Compute similarities and write into file
	with open(os.path.join(PATHS['outputs'], file), 'w') as fout:
		csvwriter = csv.writer(fout, delimiter=',')
		for n1 in neighbours:
			if(len(neighbours[n1]) == 0): continue

			for n2 in neighbours:
				if(len(neighbours[n2]) == 0): continue
				sim = len(neighbours[n1].intersection(neighbours[n2]))/len(neighbours[n1])
				print(usernames[n1], usernames[n2], sim)
				csvwriter.writerow([usernames[n1], usernames[n2], sim])

def make_adjacency_matrix(users,  direction="out", file = "adjacency.csv"):
	# Dictionary of usernames - id
	usernames = {}
	for uid in os.listdir(PATHS["names"]):
		fname = os.path.join(PATHS["names"], uid)
		with open(fname, 'r') as f:
			uname = f.readline()
			if uname in users:
				usernames[int(uid)]  = uname

	# Create a dictionary with neighbours of each user
	neighbours = {}
	try:
		for uid in usernames:
			fname = os.path.join(PATHS[direction], str(uid))
			with open(fname, 'r') as f:
				neighbours[uid] = [int(id) for line in csv.reader(f) for id in line]
	except FileNotFoundError as e:
		print(e)
		print("WARNING: Cannot create the full adjacency because some neighbourhoods are missing")
		pass

	# Compute adjacency matrix and write into file
	with open(os.path.join(PATHS['outputs'], file), 'w') as fout:
		csvwriter = csv.writer(fout, delimiter=',')
		for n in neighbours:
			for nn in neighbours[n]:	
				if(nn in usernames):
					if(direction == "out"):
						csvwriter.writerow([usernames[n], usernames[nn]])
					else:
						csvwriter.writerow([usernames[nn], usernames[n]])

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", required=False, help="A username")
    parser.add_argument("-i", "--file", required=False, help="A file with usernames")
    parser.add_argument("-f", "--follow", required=True, help="Followers or followees",
    	 				choices=['followers', 'followees'])

    args = vars(parser.parse_args())
    user = args['user']
    file = args['file']
    direction = args['follow']

    if (direction == 'followers'):
    	direction = 'in'
    if (direction == 'followees'):
    	direction = 'out'

    while(True): 
        try:
        	if(file):
        		with open(file, 'r') as f:
        			users = []
        			csvreader = csv.reader(f, delimiter=' ')
        			for i, row in enumerate(csvreader):
        				user = row[0]
        				print(i, user)
	        			userid = api.get_user(user).id
	        			fetch_neighbours(userid, direction=direction)

	        			with open(os.path.join('screen_names', str(userid)), 'w') as f:
	        				f.write(user)

	        			users.append(user)

        		print("Creating similarity matrix")
        		make_similarity_matrix(users)

        		print("Creating adjacency matrix")
        		make_adjacency_matrix(users)


        	else:
        		userid = api.get_user(user).id
        		fetch_neighbours(userid, direction=direction)

	        	with open(os.path.join('screen_names', str(userid)), 'w') as f:
	        		f.write(user)
        	

        	break
        except TweepError as e:
            print(e)
            time.sleep(60)