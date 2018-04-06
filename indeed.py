import csv
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
	
	fieldnames = ['ID', 'Role', 'URL']
		
	with open('csv_files/data.csv', 'a', encoding='utf8', newline='') as csvfile:
		writer = csv.writer(csvfile)

		if csvfile.tell() == 0:
			writer.writerow(fieldnames)
	
		urls = []
		keywords = ['Lead', 'Manager', 'Test', 'QA']

		for id, info in enumerate(source.find_all("div",  {"class": ["row", "result", "clickcard"]}), start = 1):
			link = info.find('h2', class_= 'jobtitle').find('a')
			title = link['title']
			for i in keywords:
				if i in title:
					page = 'http://www.indeed.com' + link['href']
					if page not in urls:
						urls.append(page)
						writer.writerow([id, title, page])
						break

					
def find_no_pages(source):
	for table in source.find_all('td', {'id' : 'resultsCol'}):
		pages = table.find('div', class_ = 'resultsTop').find('div', attrs={'id':'searchCount'}).get_text()
		number = pages[-3:]
		no_pages = int(number) / 50
		page_no = math.ceil(no_pages)
	return(page_no)


if __name__ == '__main__':
	
	f = open("csv_files/data.csv", "w")
	f.truncate()
	f.close()
	
	role = input('Enter role: ')
	url = getPageSource('https://ie.indeed.com/jobs?as_and=' + role + '&radius=25&l=Dublin&fromage=7&limit=50&sort=date')
	no_pages = find_no_pages(url)
    
	for i in range(no_pages):
		source = getPageSource('https://ie.indeed.com/jobs?as_and=' + role + '&radius=25&l=Dublin&fromage=7&limit=50&sort=date&start=' + str(i*50))
		find_info(source)