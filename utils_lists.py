# Creates a file with usernames of a list members
import yaml
import tweepy
import argparse
import csv
import os
from tweepy import TweepError

with open('config_neighbours.yml', 'r') as f:
    doc = yaml.load(f)
    CONSUMER_KEY = doc["CONSUMER_KEY"]
    CONSUMER_SECRET = doc["CONSUMER_SECRET"]


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_delay=60)



def download_list(user, lista, file):
	print(lista, "api...")
	users  = tweepy.Cursor(api.list_members, user, lista).items()
	with open(file, 'w') as f:
		csvwriter = csv.writer(f, delimiter=' ')
		for user in users:
			csvwriter.writerow([user.screen_name])

if __name__ == '__main__':
    
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--user", required=False, help="User")
	parser.add_argument("-l", "--list", required=False, help="List")
	parser.add_argument("-f", "--file", required=False, help="Output file")
	args = vars(parser.parse_args())
	user = args['user']
	lista = args['list']
	file = args['file']
	if file == None:
		file = lista

	download_list(user, lista, file)