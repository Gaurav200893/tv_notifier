#! /usr/bin/env python3
import os
# environnement vars
os.environ.setdefault('XAUTHORITY', '/home/user/.Xauthority')
os.environ.setdefault('DISPLAY', ':0.0')

import urllib.request
import bs4 as bs
import datetime
from dateutil.parser import parse
import notify2
import re

#get days remaining
def days_remianing(episode_date, current_date):
	date_episode = episode_date
	date_today = current_date
	difference = abs((date_episode - date_today).days)
	return str(difference)

#get ratings from description page
def getRatings(link):
	rating = '0'
	souce = urllib.request.urlopen("http://www.imdb.com"+link)
	soup = bs.BeautifulSoup(souce, 'lxml')
	rating_ele = soup.select('span[itemprop=ratingValue]')

	#if rating is present
	if len(rating_ele):
		rating = rating_ele[0].text

	return rating


#web scrappng for tv series The Flash on imdb
def tvNotifier():
	
	#get current year
	current_year = str(datetime.datetime.now().year)
	
	#craw the page
	souce = urllib.request.urlopen("http://www.imdb.com/title/tt3107288/episodes?year="+current_year)
	soup = bs.BeautifulSoup(souce, 'lxml')

	upcoming_episode = {}

	#traverse the tree
	for div in soup.find_all('div',class_="info"):
		#select release date
		air_date = div.find_all('div',class_='airdate')
		if(parse(air_date[0].text.strip()).date() >= datetime.datetime.now().date()):
			#get the name of episode
			episode_title = div.a.get("title")

			#get rating
			details_link = div.a.get("href")
			rating = getRatings(details_link)
			
			#release date
			releasing = air_date[0].text.strip()

			#create dictionary
			upcoming_episode['episode_title'] = episode_title
			upcoming_episode['releasing'] = releasing
			upcoming_episode['days_remains'] = days_remianing(parse(air_date[0].text.strip()).date(), datetime.datetime.now().date()) 
			upcoming_episode['rating'] = rating
			break

	ep_full_name = upcoming_episode['episode_title']  
	
	#prepare message
	msg = upcoming_episode['episode_title'] +"\n"+ upcoming_episode['releasing'] + \
			'\n'+ upcoming_episode['days_remains']+\
			" days to go"+ \
			"\nCurrent Rating: "+upcoming_episode['rating'] + "/10"
	print(msg)
	#use notifier to inform in ubantu
	notify2.init('foo')
	n = notify2.Notification("TV: THE FLASH",
                         msg,
                         "dialog-information" 
                        )
	n.show()


if __name__ == '__main__':
    tvNotifier()

