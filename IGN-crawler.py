import time
import requests
from bs4 import BeautifulSoup



def trade_spider(max_pages):
	startIndex = 0
	f = open('IGN.csv','w')
	while startIndex <= max_pages:
		url = 'http://www.ign.com/games/reviews?platformSlug=pc&startIndex='+ str(startIndex) +'&sortBy=score'
		source_code = requests.get(url)
		plain_text = source_code.text
		soup = BeautifulSoup(plain_text)
		for link in soup.findAll('h3'):
			temp = link.find('a')
			href = 'http://www.ign.com/' + temp.get('href')
			time.sleep(.5)
			get_single_item_data(href,f)
		startIndex += 25


def get_single_item_data(item_url,f):
	url = item_url
	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)
	
	h1 = soup.find('h1')
	title = h1.find('a').string.strip()
	
	gameInfo = soup.findAll('div', {'class': 'gameInfo-list'})
	
	temp = gameInfo[0].find('div').get_text().strip()
	temp = temp.split(': ')
	releaseDate = temp[1]	

	link = gameInfo[0].find('a')
	esrb = ''
	if link is not None:
		esrb = link.string.strip().split(' ')[0]
	
	temp = gameInfo[1].findAll('div')

	genre = temp[0].find('a')
	if genre is not None:
		genre = genre.string.strip()
	else:
		genre = ''
	
	publisher = ''
	if len(temp)>1:
		publisher = temp[1].find('a')
		if publisher is not None:
			publisher = publisher.string.strip()

	developer = ''
	if len(temp)>2:
		developer = temp[2].find('a')
		if developer is not None:
			developer = developer.string.strip()
	
	rating = soup.findAll('div', {'class': 'ratingValue'})
	if len(rating)<2:
		return
	ign = rating[0].get_text().strip()
	community = rating[1].get_text().strip()	
	f.write(title+','+releaseDate+','+esrb+','+genre+','+publisher+','+developer+','+ign+','+community+'\n')


trade_spider(5000)
