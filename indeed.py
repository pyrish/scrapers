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


def find_info(source):
	
	urls = []
	keywords = ['Lead', 'LEAD', 'Manager', 'MANAGER']
	
	for info in source.find_all("div",  {"class": ["row", "result", "clickcard"]}):
		link = info.find('h2').find('a')
		title = link.get_text()
		for i in keywords:
			if i in title:
				urls.append(link['href'])
				print('Title: ' + str(title.encode('UTF-8')))
				print('http://www.indeed.com' + link['href'])
	return(urls)
										
										

def find_no_pages(url):
  pagination = []
  for table in url.find_all('td', {'id' : 'resultsCol'}):
    pages = table.find('div', class_ = 'pagination')
    for a in pages.find_all('a'):
      span = a['href']
      pagination.append(str(span))
    pagination.pop()
  return(pagination)
  

if __name__ == '__main__':
	role = input('Enter role: ')
	url = getPageSource('https://ie.indeed.com/jobs?as_and=' + role + '&radius=25&l=Dublin&fromage=7&limit=50&sort=date')
	no_pages = find_no_pages(url)
    
	for i in no_pages:
		source = getPageSource('https://ie.indeed.com' + i)
		find_info(source)