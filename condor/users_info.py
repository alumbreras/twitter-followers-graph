import yaml
import argparse
import tweepy
import os
import csv
import time
from tweepy import TweepError
from utils import fetch_neighbours, make_similarity_matrix, make_adjacency_matrix
import pprint as pp

with open('config_neighbours.yml', 'r') as f:
    doc = yaml.load(f)
    CONSUMER_KEY = doc["CONSUMER_KEY"]
    CONSUMER_SECRET = doc["CONSUMER_SECRET"]


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=60)

def fetch_users(file):
	users = []
	with open(file, 'r') as f:
		csvreader = csv.reader(f, delimiter=' ')
		for i, row in enumerate(csvreader):
			users.append(row[0])
			

	u = api.get_user(users[0])
	print(u.screen_name)
	print(u.name)
	print(u.description)
	print(u.url)
	print(u.location)
	print(u.created_at)
	print(u.statuses_count)
	print(u.followers_count)
	print(u.friends_count)
	print(u.favourites_count)

	fname = screen_name + '.yml'
	with open(screen_name, 'w') as f:
    	yaml.dump(user_info, f, default_flow_style=False)
    	
file = "missing.csv"
fetch_users(file)