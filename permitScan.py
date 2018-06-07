#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a dumb script I wrote while waiting for city of austin permits.
   It checks the site for changes on the permit status page by naively checking
   the words on the page and creating a diff. Its not meant to be very useful for
   much else

   Writes a file with the name 'site' in the working directory to keep track of the last scrape.
   Pulls the contents of this file and compares with a new scrape to determine if changes exist
   Displays all the words in the tracked elements and shows a diff value in left column."""

from bs4 import BeautifulSoup
import difflib
import os.path
from requests_html import HTMLSession

url = 'https://abc.austintexas.gov/web/permit/public-search-other?t_detail=1&t_selected_folderrsn=11954325&t_selected_propertyrsn=5575072'

if os.path.exists('site'):
	f = open('site', 'r+')
else:
	f = open('site', 'w+')

# Get new content and check for changes
r = HTMLSession().get(url)
soup = BeautifulSoup(r.text, "lxml")
site_parse = ''
for element in soup.body.find_all('span'):
	site_parse += element.text

diff = difflib.ndiff(str.split(f.read()), str.split(site_parse))

hasChanges = False
for value in diff:
	if value.startswith('+') or value.startswith('-'):
		hasChanges = True
	print(value)
print('Has changes: ' + str(hasChanges))

# Update the saved file. I know I join something that was once a string here... probably bad
f.seek(0)
f.write(site_parse)
f.truncate()
