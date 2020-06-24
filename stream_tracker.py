#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Track keyword in twitter stream.
import argparse
import tweepy
import datetime
import codecs
import yaml
import json
import os
from config import PATHS

with open('config_keywords.yml', 'r') as f:
    doc = yaml.load(f)
    CONSUMER_KEY = doc["CONSUMER_KEY"]
    CONSUMER_SECRET = doc["CONSUMER_SECRET"]
    ACCESS_TOKEN = doc["ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = doc["ACCESS_TOKEN_SECRET"]
    

class MyStreamListener(tweepy.StreamListener):
    
    def on_status(self, status):
        #hahstags = status.entities.get('hashtags')
        #hashtags = [{'text': keywords[0][1:]}]
        keyword = keywords[0]

        coordinates = status.coordinates
        epochs = (status.created_at - datetime.datetime(1970,1,1)).total_seconds()
        user = status.user.screen_name
        user_id = status.user.id
        user_location = status.user.location
        text = status.text
        print(text)

        #fname = keyword + '.txt'
        #line = "LINE:" + user + '\t' + str(user_id) + '\t' + str(epochs) + '\t' + text + '\n'
        #with codecs.open('./tracked/'+ fname, "a", "utf-8") as f:
        #    f.write(line)
            
        fname = keyword + '.json'
        with codecs.open('./tracked/' + fname, "a", "utf-8") as f:
            data = {}
            data['user'] = user
            data['user_id'] = user_id
            data['user_location'] = user_location
            data['timestamp'] = epochs
            data['text'] = text
            f.write(json.dumps(data, indent = 4, ensure_ascii=False))
            f.write(",")


def stream_track(keywords):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=keywords, async=False) # block the main thread


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--keywords", required=True, help="keywords to track")
    args = vars(parser.parse_args())
    global keywords 
    keywords = [args['keywords']]
    print(keywords)
    stream_track(keywords)


