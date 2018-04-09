import csv
import pandas as pd
from operator import itemgetter
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
	urls = []
	keywords = ['Lead', 'Manager', 'Test', 'QA']

	for info in source.find_all("td",  {"id": "resultsCol"}):
			for div in info.find_all('div', {"class": ["row", "result", "clickcard"]}):
				d = {}
				link = div.find('h2', class_= 'jobtitle').find('a')
				role = link.get_text()
				for i in keywords:
						if i in role:
								try:
									d["1.Company"] = div.find('span', class_= 'company').get_text().strip()
								except:
									pass
								d["2.Role"] = link.get_text()
								d["3.Page"] = 'http://www.indeed.com' + link['href']
								try:
									d["4.Date"] = div.find('span', class_= 'date').get_text().strip()
								except:
									pass
								if d["3.Page"] not in urls:
										urls.append(d["3.Page"])
										break
				l.append(d)
			df = pd.DataFrame(l)
			df=df.dropna()
			df.to_csv("csv_files/pandas_data.csv")

	
def find_no_pages(source):
	for table in source.find_all('td', {'id' : 'resultsCol'}):
		pages = table.find('div', class_ = 'resultsTop').find('div', attrs={'id':'searchCount'}).get_text()
		number = pages[-3:]
		no_pages = int(number) / 50
		page_no = math.ceil(no_pages)
	return(page_no)


if __name__ == '__main__':
	
	role = input('Enter role: ')
	url = getPageSource('https://ie.indeed.com/jobs?as_and=' + role + '&radius=25&l=Dublin&fromage=7&limit=50&sort=date')
	no_pages = find_no_pages(url)
    
	for i in range(no_pages):
		source = getPageSource('https://ie.indeed.com/jobs?as_and=' + role + '&radius=25&l=Dublin&fromage=7&limit=50&sort=date&start=' + str(i*50))
		find_info(source)