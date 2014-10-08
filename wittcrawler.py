# To do: write bot. Parse out sentences using reg ex and delete duplicates
# Check whether sentence has been tweeted before: if it hasn't, tweet it!
# Do all of this in a cron job

import requests
from bs4 import BeautifulSoup
import re

def make_soup(url):
	r = requests.get(url)
	page = r.text # Get the text contents of the page 
	soup = BeautifulSoup(page)
	return soup 

soup = make_soup("http://tractatus-online.appspot.com/Tractatus/jonathan/body.html")
aphorisms = soup.findAll("dd")

strippedList = []
for aphorism in aphorisms:
	aphorism = aphorism.get_text() # Strip out all of the HTML 
	aphorism = aphorism.replace("\r", "") # Strip out carriage returns and new line characters
	aphorism = aphorism.replace("\n", "")
	strippedList.append(aphorism)

def split_soup_elements(list):
	# Takes a list of the strings scraped from the web page and splits elements with more than one sentence using reg ex

	fullListOfMatches = []
	for item in list:
		# All matches that begin with A-Z or 0-9, contain zero or more of any character, and end with ".", "?" or "!" not followed by another alphanumeric character 
		matches = re.findall("[A-Z0-9].*?[\?\.!]", item) 
		fullListOfMatches += matches

	for item in fullListOfMatches:
		itemCount = fullListOfMatches.count(item)
		if itemCount > 1:
			fullListOfMatches.remove(item) 

	return fullListOfMatches


finalList = split_soup_elements(strippedList)
print(finalList)
