# To do: write bot. Parse out sentences using reg ex and delete duplicates
# Check whether sentence has been tweeted before: if it hasn't, tweet it!
# Do all of this in a cron job

import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
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
	strippedList.append(aphorism)

print(strippedList)

# print(list(OrderedDict.fromkeys(strippedList)))
