#!/usr/bin/python3
from pyvirtualdisplay import Display

import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup


def make_soup(driver, url):

	driver.get(url)
	soup = BeautifulSoup(driver.page_source,'html.parser')

	return(soup)


def hubspot(driver):
	
# Pull Jobs from Hubspot

	fieldnames = ['ID', 'Company', 'Role', 'Department', 'Location', 'URL']

	with open('csv_files/data_companies.csv', 'a', encoding='utf8', newline='') as csvfile:
		writer = csv.writer(csvfile)

		if csvfile.tell() == 0:
			writer.writerow(fieldnames)

		page = make_soup(driver,'https://www.hubspot.com/jobs/locations/dublin')
		company = page.find('h2', class_= 'section-header__header section-header--divider').get_text()
		roles_hubspot = []
		
		for a in page.find_all('li', class_= 'career--listings__line-item'):
			#role = a.find('div').find('p').get_text()
			role_hubspot = a.find('div', class_= 'line-item--title').get_text()
			department = a.find('div', class_= 'line-item--department').get_text()
			location = a.find('div', class_= 'line-item--location').get_text()
			
			for link in a.find_all('a', href=True):
				if 'Manager' in role_hubspot:
					url = link['href']
					roles_hubspot.append(role_hubspot)
					writer.writerow([len(roles_hubspot), company, role_hubspot, department, location, url])

# Pull Jobs from Facebook
	
def facebook(driver):	
		
		fieldnames = ['ID', 'Company', 'Role', 'Department', 'Location', 'URL']

		with open('csv_files/data_companies.csv', 'a', encoding='utf8', newline='') as csvfile:
			writer = csv.writer(csvfile)

			if csvfile.tell() == 0:
				writer.writerow(fieldnames)


			page = make_soup(driver,'https://www.facebook.com/careers/locations/dublin/')
			fb_base_url = 'https://www.facebook.com'
			location = page.find('h3', {"class": ["_3m9", "_1zbm", "_3o70", "_3y1f", "_4_n2"]}).get_text()
			company = page.find('i', {"class": ["fb_logo"]}).get_text()
			roles_fb = []

			for div in page.find_all('div', class_= '_4hnn'):
				for link in div.find_all('a', href=True):
					for role_fb in ROLES:
						if role_fb in link.text:
							roles_fb.append(role_fb)
							position = (link.text)
							department = (div.parent.get('id')).replace('div','')
							url = fb_base_url + link['href']
							writer.writerow([len(roles_fb), company, position, department, location, url])

################################################################################

if __name__ == '__main__':
	
	f = open("data_companies.csv", "w")
	f.truncate()
	f.close()

	ROLES = ['Quality', 'Project', 'Test', 'Release']

	display = Display(visible=0, size=(1920, 1080)).start()
	driver = webdriver.Firefox()

	hubspot(driver)
	#facebook(driver)
	
	driver.close()