from os import listdir
import os
import json

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


PATHS = {"in": "./followers/",
         "out": "./followees/",
         "names": "./screen_names/",
         "tracked": "./tracked/",
         "outputs": "./outputs/"}


		
def get_users(direction="in"):
	"""Show users whose followers have already been tracked"""
	
	# Fetched users
	userids = []
	for userid in listdir(PATHS[direction]):
		userids.append(userid)

	# Dictionary of all known id - usernames
	usernames = {}
	for userid in listdir(PATHS["names"]):
		fname = os.path.join(PATHS["names"], userid)
		with open(fname, 'r') as f:
			usernames[userid]  = f.readline()


	# Names of fetched users
	users = []
	for uid in userids:
		if uid  in usernames:
			users.append(usernames[uid])

	return sorted(users)


def get_participants(keyword):
    participants = {}
    with open('tracked/' + keyword + ".json", 'r') as f:
    	data = json.load(f)
    	for entry in data:
    		if entry["user_id"] not in participants:
    			participants[entry["user_id"]] = entry['user']

    return participants

def make_dataset_participations():
	# Get all .json file names
	filenames = listdir(PATHS["tracked"])
	with open(os.path.join(PATHS['outputs'], 'participations.txt'), 'w') as fout:
		csvwriter = csv.writer(fout, delimiter=',')

		for i, f in enumerate(filenames):
			print(f)
			participants = get_participants(f[:-5])
			for p in participants.values():
				csvwriter.writerow([p, i, 1]) 

if __name__ == '__main__':
    
	users = get_users()
	#make_dataset_participations()