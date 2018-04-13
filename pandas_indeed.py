import csv
import pandas as pd
import math
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


def find_info(source):
	l = []
	for info in source.find_all("td",  {"id": "resultsCol"}):
			for div in info.find_all('div', {"class": ["row", "result", "clickcard"]}):
				d = {}
				link = div.find('h2', class_= 'jobtitle').find('a')
				role = link.get_text()
				d["Company"] = div.find('span', class_= 'company').get_text().strip()
				d["Role"] = role
				d["URL"] = 'http://www.indeed.com' + link['href']
				d["Date"] = div.find('span', class_= 'date').get_text().strip()
				l.append(d)
			df = pd.DataFrame(l)
			df = df[['Date', 'Company', 'Role', 'URL']]
			df=df.dropna()
			df.sort_values(by=['Date'], inplace=True, ascending=False)
			df.to_csv("csv_files/pandas_data.csv")


if __name__ == '__main__':
	
	role = input('Enter role: ')
	url = getPageSource('https://ie.indeed.com/jobs?as_and=' + str(role) +'&radius=25&l=Dublin&fromage=7&limit=50&sort=date&start=0')

	find_info(url)