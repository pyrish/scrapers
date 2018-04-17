#!/usr/bin/python3

import csv
import pandas as pd
import os
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
	l = []
	for b in soup.find_all('div', class_= 'jobInfo'):
		d = {}
		company = b.find('h2').find('a')
		d["Role"] = company['title'].split(':')[0]
		d["URL"] = 'https://www.computerjobs.ie' + company['href']
		company_name = b.find('ul', class_= 'jobDetails').find('li', class_= 'jobCompanyName').get_text()
		d["Company"] = company_name.split(':')[1].strip()
		date = b.find('ul', class_= 'jobDetails').find('li', class_= 'jobLiveDate').get_text()
		d["Date"] = date.split(':')[1].strip()
		l.append(d)
	return l

if __name__ == '__main__':
	
	display = Display(visible=0, size=(1920, 1080)).start()
	
	f = open("csv_files/pandas_data.csv", "w")
	f.truncate()
	f.close()
	
	os.system('clear')
	
	print('\n')
	print('#############################################################')
	print('Computerjobs.ie Job Scraper - Copyright Mariano Vazquez, 2018')
	print('#############################################################')
	print('\n')
	
	query = input('Enter role to search: ')
	print('\nLooking for Jobs, please wait...')
	print('\n')
	pholder_page = 'https://www.computerjobs.ie/jobboard/cands/JobResults.asp?c=1&strKeywords='+query+'&lstPostedDate=3&lstRegion=Central+Dublin&lstRegion=South+Dublin&lstRegion=North+Dublin&lstRegion=West+Dublin&pg=1'
	code = getPageSource(pholder_page)
	no_pages = get_number_pages(code)
	
	new_page = 'https://www.computerjobs.ie/jobboard/cands/JobResults.asp?c=1&strKeywords='+query+'&lstPostedDate=3&lstRegion=Central+Dublin&lstRegion=South+Dublin&lstRegion=North+Dublin&lstRegion=West+Dublin&pg='
	
	l = []
	for i in range(no_pages):
		page = new_page + str(i+1)
		soup = getPageSource(page)
		print("Scraping Page number: " + str(i+1))
		l.extend(find_data(soup))
	
	df = pd.DataFrame(l)
	df = df[['Date', 'Company', 'Role', 'URL']]
	df=df.dropna()
	df.sort_values(by = ['Date'], inplace=True, ascending=False)
	df.to_csv("csv_files/pandas_data.csv", mode='a', header=True, index=False)
	
	print("\nDone!!, check the CSV File!")