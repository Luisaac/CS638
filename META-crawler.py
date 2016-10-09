import requests
import urllib2
import urllib
import os
from bs4 import BeautifulSoup




def trade_spider(max_pages):
	pageNum = 0
	f = open('META.csv','w')
	counter = -1
	number = 0
	while pageNum <= max_pages:
		url = 'http://www.metacritic.com/browse/games/release-date/available/pc/metascore?view=condensed&page='+str(pageNum)
		hdr = {'User-Agent': 'Mozilla/5.0'}
		req = urllib2.Request(url,headers=hdr)
		page = urllib2.urlopen(req)
		soup = BeautifulSoup(page)
		soup1 = soup.find('ol',{'class' : 'list_product_condensed'})
		for link in soup1.findAll('a'):
			href ='http://www.metacritic.com/'+link.get('href')
			if(get_single_item_data(href, f, number) == 1):
				s = 'dir'+str(counter)
				if(number%100 == 0):
					counter += 1
					s = 'dir' + str(counter)
					os.makedirs(s)
				urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
				urllib.urlretrieve(href, s +'/'+href.replace('/','@')+'.html')
				number+=1
		pageNum+=1


def get_single_item_data(item_url,f,num):
	url = item_url
	hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(url,headers=hdr)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)
	info = soup.findAll('span',{'itemprop' : 'name'})
	title = info[0].get_text().strip().replace(',','')
	
	releaseDate = soup.find('span',{'itemprop' : 'datePublished'})
	releaseDate = releaseDate.get_text().strip()
	
	esrb = soup.find('span',{'itemprop' : 'contentRating'})
	if(esrb is None):
		esrb = ''
	else:
		esrb = esrb.get_text()

	genre = soup.find('span',{'itemprop' : 'genre'})
	if(genre is None):
		genre = ''
	else:
		genre = genre.get_text().strip()
	if(len(info) < 2):
		publisher = ''
	else:
		publisher = info[1].get_text().strip().replace(',','')
	
	
	developer = soup.find('li',{'class' : 'developer'})
	if(developer is None):
		developer = ''
	else:
		developer = developer.find('span',{'class': 'data'})
		if(developer is None):
			developer = ''
		else:
			developer = developer.get_text().strip().replace(',','')


	metaScore = soup.find('span',{'itemprop' : 'ratingValue'})
	if(metaScore is None):
		metaScore = ''
	else:
		metaScore = metaScore.get_text()

	user = soup.find('div',{'class' : 'userscore_wrap'})
	user = user.find('div',{'class' : 'metascore_w'})
	if(user is None):
		user = ''
	else:
		user = user.get_text()
	
	try:
		f.write(str(num)+','+title+','+releaseDate+','+esrb+','+genre+','+publisher+','+developer+','+metaScore+','+user+'\n')
	except UnicodeEncodeError:
		return 0
	return 1

trade_spider(14)


