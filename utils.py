# Common functions

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


##################################################
# Functions that fetch neighbours and screen names
##################################################
		
def api_neighbours_ids(user, api, direction="in"):
    if direction == "in":
        neighbours_ids = api.followers_ids(user)

    else:
        neighbours_ids = api.friends_ids(user)

    return neighbours_ids

def fetch_neighbours(userid, api, direction="in"):
    fname = os.path.join(PATHS[direction], str(userid))

    # If user is already tracked, get their followers from file
    if os.path.isfile(fname):
        print("User had already been fetched\n")

    # otherwise use the API
    else:
        try:
            with open(fname, 'w') as f:
                neighbours = api_neighbours_ids(userid, api, direction)                
                csv.writer(f).writerow(neighbours)
        except TweepError as e:
            print(e)
            if e == "Not authorized.":
                writer.writerow("")

def screen_names(users, api):
    """Get the screen name of ego's neighbours"""
    
    # Get screen_name of each neighbour and store in into a file    
    n_users = len(users) + 1
    batch_start = 0
    batch_end = min(100, n_users)
    while(batch_start < n_users):
        try:
        	#users_batch = api.lookup_users(screen_names=users[batch_start:batch_end])
        	users_batch = api.lookup_users(users[batch_start:batch_end])
        	for u in users_batch:
        		print(u.screen_name, u.id)
        		with open(os.path.join('screen_names', str(u.id)), 'w') as f:
        			f.write(u.screen_name)
        except TweepError as e:
        	print(e)
        	time.sleep(60)

        batch_start += 100
        batch_end = min(batch_end+100, n_users)


###############################################
# Functions that create the final datasets
###############################################
def make_similarity_matrix(users, direction = "out", file = "similarities.csv"):
	""" 
		Build a similarity matrix user_a, user_b
		with the percentage of similar neighbours
	"""

	# Dictionary of usernames - id
	usernames = {}
	if(type(users[0]) == str):
		for uid in os.listdir(PATHS["names"]):
			uid = int(uid)
			fname = os.path.join(PATHS["names"], str(uid))
			with open(fname, 'r') as f:
				uname = f.readline()
				if uname in users:
					usernames[uid]  = uname
	else:
		for uid in os.listdir(PATHS["names"]):
			uid = int(uid)
			fname = os.path.join(PATHS["names"], str(uid))
			if uid in users:
				with open(fname, 'r') as f:
					uname = f.readline()
					usernames[uid]  = uname


	# Create a dictionary with neighbours of each user
	neighbours = {}
	for uid in usernames:
		fname = os.path.join(PATHS[direction], str(uid))
		with open(fname, 'r') as f:
			n_neighbours = set([int(id) for line in csv.reader(f) for id in line])
			if(len(n_neighbours)>1000):
				neighbours[uid] = n_neighbours

	# Compute similarities and write into file
	with open(os.path.join(PATHS['outputs'], file), 'w') as fout:
		csvwriter = csv.writer(fout, delimiter=',')
		csvwriter.writerow(["Source", "Target", "Weight"])
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

	if(type(users[0]) == str):
		for uid in os.listdir(PATHS["names"]):
			uid = int(uid)
			fname = os.path.join(PATHS["names"], str(uid))
			with open(fname, 'r') as f:
				uname = f.readline()
				if uname in users:
					usernames[uid]  = uname
	else:
		for uid in os.listdir(PATHS["names"]):
			uid = int(uid)
			fname = os.path.join(PATHS["names"], str(uid))
			if uid in users:
				with open(fname, 'r') as f:
					uname = f.readline()
					usernames[uid]  = uname


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



def graph_ego(ego_screenname, api, direction="in"):
    """Build the a graph of the egonet of ego in Gephi format"""

    
    ego = api.get_user(ego_screenname).id
    
    all_neighbours = {}
    screen_names = {}

    # Read ego_alters from file    
    with open(os.path.join(PATHS[direction], str(ego)), 'r') as f:
        ego_neighbours = [int(id) for line in csv.reader(f) for id in line]

    # A dictionary to store ego neighbours and neighbours of neighbours
    # We can already fill it with the ego neighbours
    all_neighbours = {}
    all_neighbours[ego] = ego_neighbours
    
    # A dictionaty that will map ids to screen_names
    # we can already fill it with the ego screen_name
    screen_names = {}
    screen_names[ego] = ego_screenname
    
    # Fill both dictionaries with information stored in files
    for u in all_neighbours[ego]:
        fname = os.path.join(PATHS[direction], str(u))
        try:
            with open(fname, 'r') as f:
                all_neighbours[u] = [int(id) for line in csv.reader(f) for id in line]
        except IOError:
            pass # neighbours of this user not yet fetched
            
        fname = os.path.join('screen_names', str(u))
        try:
            with open(fname, 'r') as f:        
                screen_names[u] = f.read()
        except IOError:
            pass # screen name of this user not yet fetched
            
    # Create graphML
    print("Writing graph...")
    path = './outputs/'
    if not os.path.exists(path):
        os.makedirs(path)
    
    with open(path + ego_screenname + "_" + direction + '.graphml', 'w') as out:
        # header
        out.write("""<?xml version="1.0" encoding="UTF-8"?>
        <graphml xmlns="http://graphml.graphdrawing.org/xmlns"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns
        http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">
        \n""")
        
        # General specifications
        out.write("""<key id="label" for="node" attr.name="label" attr.type="string" />\n""")
        out.write("""<graph edgedefault="directed">\n\n""")
    
        # Add nodes (ego plus one node for each neighbours)
        # if we don't have its screen_name, use its user id as name
        out.write("<node id='%d'><data key='label'>%s</data></node>\n" % (ego, escape(screen_names[ego])))
        for f_id in all_neighbours[ego]:
                if f_id in screen_names:
                    screen_name =  escape(screen_names[f_id])
                else:
                    screen_name =  f_id                
                out.write("<node id='%d'><data key='label'>%s</data></node>\n" % (f_id, screen_name))
         
        edge_id = 0
        
        neighbourhood = all_neighbours[ego]
        neighbourhood.append(ego)
        
        # Add edges to ego and between ego neighbours
        for f_id, ff_ids in all_neighbours.items():
            for ff_id in set(ff_ids).intersection(neighbourhood):
                if(direction == "in"):
                    out.write("<edge id='edge%d' source='%d' target='%d' />\n" % (edge_id, ff_id, f_id))
                else:
                    out.write("<edge id='edge%d' source='%d' target='%d' />\n" % (edge_id, f_id, ff_id))                    
                edge_id += 1
        
        # Close graphml object
        out.write("</graph></graphml>")