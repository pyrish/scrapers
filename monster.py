#!/usr/bin/python3
#from pyvirtualdisplay import Display

import csv
from bs4 import BeautifulSoup
import urllib.request


def getPageSource(current_page):
	
	hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
	req = urllib.request.Request(current_page, headers=hdr)
	page = urllib.request.urlopen(req)
	
	soup = BeautifulSoup(page, "html5lib")
	return(soup)


def find_data(source):
	fieldnames = ['ID', 'Role', 'URL']
		
	with open('data.csv', 'w', encoding='utf8', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(fieldnames)

		for id, a in enumerate(source.find_all('div', class_= 'jobTitle'), start=1):
			pholder = a.find('h2').find('a')
			url = pholder['href']
			role = pholder.get_text().strip()
			writer.writerow([id, role, url])

#date = source.find('div', class_= 'job-specs-date').find('p').get_text()
# for company in div.find_all('div', class_= 'company'):
# 		company_name = company.find('a').find('span').get_text()


if __name__ == '__main__':
  
	query = input('Enter role to search: ')

	source = getPageSource('https://www.monster.ie/jobs/search/?q='+query+'&where=Dublin__2C-Dublin&sort=dt.rv.di&page=1')
	find_data(source)
	
		
		
		
		
		
		
		
		
		
		
		