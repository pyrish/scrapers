import pandas as pd
import os
from bs4 import BeautifulSoup
import urllib.request

# Make soup function
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


# Find number of pages to be scraped
def find_pages(source):
	pages = []
	base_url = 'https://ie.indeed.com'
	for a in source.find_all('div', class_= 'pagination'):
		for link in a.find_all('a', href=True):
			pages.append(base_url + link['href'])
	pages.insert(0, base_url + '/jobs?q=test&l=Dublin&sort=date&limit=50&radius=25&start=0')
	pages.pop()
	return pages


# Pull information from only one page
def find_info(source):
	l = []
	for info in source.find_all("td",  {"id": "resultsCol"}):
			for div in info.find_all('div', {"class": ["row", "result", "clickcard"]}):
				d = {}
				try:
					link = div.find('h2', class_= 'jobtitle').find('a')
					role = link.get_text()
					d["Company"] = div.find('span', class_= 'company').get_text().strip()
					d["Role"] = role
					d["URL"] = 'http://www.indeed.com' + link['href']
					d["Date"] = div.find('span', class_= 'date').get_text().strip()
					l.append(d)
				except:
					pass
	return l


if __name__ == '__main__':
	
	f = open("csv_files/pandas_data.csv", "w")
	f.truncate()
	f.close()
	
	os.system('clear')
	
	print('\n')
	print('#######################################################')
	print('Indeed.ie Job Scraper - Copyright Mariano Vazquez, 2018')
	print('#######################################################')
	print('\n')
	
	role = input('Enter role: ')
	max_pages = int(input('Enter number of pages to scrape: '))
	print('\nScraping your results, please wait...')
	url = getPageSource('https://ie.indeed.com/jobs?as_and=' + str(role) +'&radius=25&l=Dublin&limit=50&sort=date')
	pages = find_pages(url)
	
	# Iterate through the pages
	l_main = []
	for i in pages[:max_pages]:
		source = getPageSource(i)
		l_main.extend(find_info(source))
	
	# Put all results into a DataFrame
	df = pd.DataFrame(l_main)
	df = df[['Date', 'Company', 'Role', 'URL']]
	df=df.dropna()
	df.sort_values(by=['Date'], inplace=True, ascending=False)
	df.to_csv("csv_files/pandas_data.csv", mode='a', header=True, index=False)

	print("\nDone!!, check the CSV File!")