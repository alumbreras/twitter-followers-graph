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



def screen_names(users):
    """Get the screen name of ego's neighbours"""
    
    # Get screen_name of each neighbour and store in into a file    
    n_users = len(users) + 1
    batch_start = 0
    batch_end = min(100, n_users)
    while(batch_start < n_users):
        try:
        	users_batch = api.lookup_users(screen_names=users[batch_start:batch_end])
        	for u in users_batch:
        		print(u.screen_name, u.id)
        		with open(os.path.join('screen_names', str(u.id)), 'w') as f:
        			f.write(u.screen_name)
        except TweepError as e:
        	print(e)
        	time.sleep(60)

        batch_start += 100
        batch_end = min(batch_end+100, n_users)
    print("Number of neighbours:", n_users - 1)


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
	
	usernames = []
	with open(file, 'r') as f:
		csvreader = csv.reader(f, delimiter=' ')
		for user in csvreader:
			usernames.append(user[0])
	screen_names(usernames)