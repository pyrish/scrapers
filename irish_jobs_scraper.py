#!/usr/bin/python3

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
	base_url = 'https://www.irishjobs.ie'
	fieldnames = ['ID', 'Company','Role', 'URL', 'Date']
		
	with open('data.csv', 'a', encoding='utf8', newline='') as csvfile:
		writer = csv.writer(csvfile)

		if csvfile.tell() == 0:
			writer.writerow(fieldnames)

		for id, a in enumerate(source.find_all(attrs={"itemtype" : "https://schema.org/JobPosting"}), start=1):
			job_info = a.find('h2').find('a')
			company_name = a.find('h3').find('a').get_text()
			url = job_info['href']
			full_url = (base_url + url)
			role = (job_info.get_text())
			date = a.find('li',class_='updated-time').get_text().replace('Updated','').strip()
			writer.writerow([id, company_name, role, full_url, date])

		
if __name__ == '__main__':
  
	query = input('Enter role to search: ')
	source = getPageSource('https://www.irishjobs.ie/ShowResults.aspx?Keywords='+query+'&Location=102&Category=3&Recruiter=All&SortBy=MostRecent&PerPage=100')
	
	find_data(source)
