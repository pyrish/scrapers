#!/usr/bin/python3

import csv
from bs4 import BeautifulSoup
import urllib.request

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def getPageSource(current_page):
	
	driver = webdriver.Firefox()
	driver.get(current_page)
	url_code = driver.page_source
	driver.close()
	soup = BeautifulSoup(url_code, "html5lib")
	return(soup)
			
	
def get_number_pages(soup):
	links = []
	for a in soup.find_all('a', class_= 'page-link'):
		links.append((a['href'])[-1])
	links = links[:-2]
	results = [int(i) for i in links]
	return(results)


def find_data(soup):
	companies = []
	dates = []
	fieldnames = ['ID', 'Company', 'Role', 'URL', 'Date']
		
	with open('data.csv', 'a', encoding='utf8', newline='') as csvfile:
		writer = csv.writer(csvfile)

		if csvfile.tell() == 0:
			writer.writerow(fieldnames)

		for id, b in enumerate(soup.find_all('div', class_= 'company'), start=1):
			company_name = b.find('a').find('span').get_text()
			companies.append(company_name)
			
		for id, c in enumerate(soup.find_all('div', class_= 'job-specs-date'), start=1):
			date = c.find('p').find('time').get_text()
			dates.append(date)
			
		for id, a in enumerate(soup.find_all('div', class_= 'jobTitle'), start=1):
			pholder = a.find('h2').find('a')
			url = pholder['href']
			role = pholder.get_text().strip()
			writer.writerow([id, companies[id-1], role, url, dates[id-1]])
			
		

if __name__ == '__main__':
  
	display = Display(visible=0, size=(1920, 1080)).start()
	
	f = open("data.csv", "w")
	f.truncate()
	f.close()
	
	query = input('Enter role to search: ')
	
	page = 'https://www.monster.ie/jobs/search/?q='+query+'&where=Dublin__2C-Dublin&sort=dt.rv.di&page=1'
	#soup = BeautifulSoup(open('soup.html', encoding ='utf-8'), "html5lib")
	soup = getPageSource(page)
	find_data(soup)
	no_pages = get_number_pages(soup)
	
	new_page = 'https://www.monster.ie/jobs/search/?q='+query+'&where=Dublin__2C-Dublin&sort=dt.rv.di&page='
	
	for i in no_pages:
		soup = getPageSource(new_page + str(i))
		print("Scraping Page number: " + str(i-1))
		find_data(soup)
	print("\n")
	print("Done!!, check the CSV File!")

#		Open thr file to get the source and avoid sending HTTP Requests all the time!!!!
# 	with open("soup.html", "w", encoding='utf-8') as file:
# 		file.write(str(soup))