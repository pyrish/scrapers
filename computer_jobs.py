#!/usr/bin/python3

import os.path
import sys
import operator
import csv
import math
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
  num_results = soup.find("strong").contents
  makeitastring = ''.join(map(str, num_results))
  temp = (int(makeitastring)) / 10
  page_no = math.ceil(temp)
  return(page_no)


def find_data(soup):
	
	fieldnames = ['ID', 'Company', 'Role', 'URL', 'Date']
	
	with open('data.csv', 'a', encoding='utf8', newline='') as csvfile:
		writer = csv.writer(csvfile)

		if csvfile.tell() == 0:
			writer.writerow(fieldnames)

		for id, b in enumerate(soup.find_all('div', class_= 'jobInfo'), start=1):
			company = b.find('h2').find('a')
			title = company['title'].split(':')[0]
			company_url = 'https://www.computerjobs.ie' + company['href']
			company_name = b.find('ul', class_= 'jobDetails').find('li', class_= 'jobCompanyName').get_text()
			company_name = company_name.split(':')[1].strip()
			date = b.find('ul', class_= 'jobDetails').find('li', class_= 'jobLiveDate').get_text()
			date = date.split(':')[1].strip()
			writer.writerow([id, company_name, title, company_url, date])
			#sortedlist = sorted(csvfile, key=operator.itemgetter(4), reverse=True)

if __name__ == '__main__':
  
	display = Display(visible=0, size=(1920, 1080)).start()
	
	f = open("data.csv", "w")
	f.truncate()
	f.close()
	
	query = input('Enter role to search: ')
	
	#page = 'https://www.monster.ie/jobs/search/?q='+query+'&where=Dublin__2C-Dublin&sort=dt.rv.di&page=1'
	#soup = BeautifulSoup(open('soup.html', encoding ='utf-8'), "html5lib")
	pholder_page = 'https://www.computerjobs.ie/jobboard/cands/JobResults.asp?c=1&strKeywords='+query+'&lstPostedDate=7&lstRegion=Central+Dublin&lstRegion=South+Dublin&lstRegion=North+Dublin&lstRegion=West+Dublin&pg=1'
	code = getPageSource(pholder_page)
	no_pages = get_number_pages(code)
	#find_data(soup)
	new_page = 'https://www.computerjobs.ie/jobboard/cands/JobResults.asp?c=1&strKeywords='+query+'&lstPostedDate=7&lstRegion=Central+Dublin&lstRegion=South+Dublin&lstRegion=North+Dublin&lstRegion=West+Dublin&pg='
	
	for i in range(no_pages):
		page = new_page + str(i+1)
		soup = getPageSource(page)
		print("Scraping Page number: " + str(i+1))
		find_data(soup)
	print("\n")
	print("Done!!, check the CSV File!")

#		Open thr file to get the source and avoid sending HTTP Requests all the time!!!!
# 	with open("soup.html", "w", encoding='utf-8') as file:
# 		file.write(str(code))