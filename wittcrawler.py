#!/usr/bin/env python
# -*- coding: utf-8 -*-

# To do: write bot. Parse out sentences using reg ex and delete duplicates √
# Check whether string has been tweeted before (maybe keep a log to avoid making loads of API calls). If it hasn't, tweet it! √
# Do all of this in a cron job 
# Also need to include something that splits strings over 140 chars √
# Fix encoding issues

import requests, re, time
from bs4 import BeautifulSoup
import twitterbot

def make_soup(url):

	r = requests.get(url)
	page = r.text # Get the text contents of the page 
	soup = BeautifulSoup(page)
	return soup 


def strip_formatting(aphorisms):
	'''Returns the HTML soup returned by make_soup, 
	stripped of all formatting.'''

	strippedList = []

	for aphorism in aphorisms:
		aphorism = aphorism.get_text().encode("utf-8") # Strip out all of the HTML and convert unicode to UTF-8
		aphorism = aphorism.replace("\r", "") # Strip out carriage returns and new line characters
		aphorism = aphorism.replace("\n", "")
		strippedList.append(aphorism)

	return strippedList


def split_soup_elements(strippedList):
	'''Takes a list of the strings scraped from the web page and splits elements with more than one sentence using reg ex.'''
	fullListOfMatches = []

	for item in strippedList:
		# All matches that begin with A-Z or 0-9, contain zero or more of any character, and end with ".", "?" or "!" not followed by another alphanumeric character 
		matches = re.findall("[A-Z].*?[\?\.!]", item) 
		fullListOfMatches += matches

	for item in fullListOfMatches:
		itemCount = fullListOfMatches.count(item)
		if itemCount > 1:
			fullListOfMatches.remove(item) 

	return fullListOfMatches


if __name__ == "__main__":
	soup = make_soup("http://tractatus-online.appspot.com/Tractatus/3side_by_side/body.html")
	aphorisms = soup.findAll("dd")
	strippedList = strip_formatting(aphorisms)
	fullListOfMatches = split_soup_elements(strippedList)

	# Authenticate our account, split up our content into tweets of under 140 characters, find a line that hasn't been tweeted yet, and tweet that thing!
	api = twitterbot.authenticate_account()
	tweets = twitterbot.read_content(fullListOfMatches)
	tweet = twitterbot.get_untweeted_tweet(tweets)
	twitterbot.make_post(api, tweet)