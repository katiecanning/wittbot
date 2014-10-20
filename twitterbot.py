#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy

def authenticate_account():
    '''Returns the API authorisation we need to get going.'''
     # Authentication keys are stored in a separate text file for security
     # reasons. This isn't the best method, but it'll do for now.  Here we're
     # just opening that file, getting a list of the keys and chopping off
     # newlines.
    textFile = open("secret.txt", "r")
    apiKeys = textFile.readlines()
    textFile.close()

    index = 0
    while index < len(apiKeys):
        for item in apiKeys:
            strippedItem = item.rstrip()
            apiKeys[index] = strippedItem
            index += 1

    # Now we can get the various authentication keys required and authenticate!
    # Should maybe put this in a function for future use.
    CONSUMER_KEY = apiKeys[0]
    CONSUMER_SECRET = apiKeys[1]
    ACCESS_KEY = apiKeys[2]
    ACCESS_SECRET = apiKeys[3]
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    return api

def read_content(botTextContent):
    '''Reads the raw tweet content and returns a list containing
    sub-tweets for tweets of more than 140 characters.'''
    # This function needs cleaning up. 
    
    tweets = []
    subTweets = []

    for line in botTextContent:
        length = 0
        counter = 0
        startChar = 0
        endChar = 136
        if len(line) <= 140:
            tweets.append(line)
        else:
            while length + (3 * counter) < len(line): # (3 * counter) accounts for the ellipses that have been added to each tweetSection.
                splitIndex = line.rfind(" ", startChar, endChar) # Returns last index where " " is found between indices startChar and endChar
                if counter == 0:
                    subTweets = []
                    tweetSection = line[startChar:splitIndex] + "..."
                length = sum(len(item) for item in subTweets) # Get the collective length of all of the subtweets. Bug here - it takes into account length of everything in subTweets, including subTweets of other
                if counter > 0 and counter < int((len(line) / 137) + 1): # All cases between the initial tweet section and the final tweet section
                    tweetSection = line[startChar:splitIndex] + "..." 
                elif counter == int((len(line) / 137) + 1): # The final tweet section
                    tweetSection = "..." + line[startChar:splitIndex]
                subTweets.append(tweetSection)
                startChar = splitIndex + 1
                endChar = startChar + 136
                counter += 1
                tweets = tweets + subTweets

    return tweets

def get_untweeted_tweet(tweets):
    '''Finds and returns the first example of a Tweet 
    that we haven't tweeted before by checking the logs.'''

    f = open("testbotlog.txt", "r")
    log = f.readlines()
    newLog = [item.rstrip() for item in log]
    f.close()

    tweets = [item.rstrip() for item in tweets]

    for line in tweets: # Let's find the first tweet that hasn't been tweeted yet! 
        if not line in newLog:
            return line 


def make_post(api, tweet):
    '''Tweet the bloody thing!'''

    # print(tweet)
    # print(len(tweet))
    api.update_status(tweet)
    # time.sleep(900) # Tweet every 15 minutes. Perhaps better to do this in a cron job. 
    f = open("testbotlog.txt", "a")
    # tweetTime = strftime("%d %b %Y %H %M", gmtime())
    # f.write(tweetTime + " " + line+ "\n") # This logs the time and date of the tweet
    # as well as the tweet itself. Problem is, it messes with checking the tweet logs.
    # Will fix, perhaps with reg ex, but for now we'll just leave out the time and date. 
    f.write(tweet + "\n")
    f.close()