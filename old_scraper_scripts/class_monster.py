#!/usr/bin/python3

import csv
from bs4 import BeautifulSoup
import os
import urllib.request
import pandas as pd

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Monster(object):
  def __init__(self, role):
    self.role = role
    self.url = 'https://www.monster.ie/jobs/search/?q={}&where=Dublin__2C-Dublin&sort=dt.rv.di&page='.format(role)
    self.driver = webdriver.Firefox()

  def getPageSource(self):
    self.driver.get(self.url)
    url_code = self.driver.page_source
    self.driver.close()
    soup = BeautifulSoup(url_code, "html5lib")
    return(soup)

  # def get_number_pages(soup):
  # 	links = []
  # 	for a in soup.find_all('a', class_= 'page-link'):
  # 		links.append((a['href'])[-1])
  # 	links = links[:-2]
  # 	results = [int(i) for i in links]
  # 	return(results)


  # Function to scrape all jobs per page
  def find_data(self, soup):
    l = []
    for div in soup.find_all('div', class_ = 'js_result_container'):
      d = {}
      try:
        d["Company"] = div.find('div', class_= 'company').find('a').find('span').get_text()
        d["Date"] = div.find('div', {'class':['job-specs-date', 'job-specs-date']}).find('p').find('time').get_text()
        pholder = div.find('div', class_= 'jobTitle').find('h2').find('a')
        d["URL"] = pholder['href']
        d["Role"] = pholder.get_text().strip()
        l.append(d)
      except:
        pass
    return l

  # Iterates through the pages
  def iterate_pages(self):
    max_pages = int(input('Enter number of pages to search: '))
    print('\nScraping list of jobs, please wait...')
    print('\n')
    l_main = []
    for i in range(max_pages):
      page = self.url + str(i+1)
      html_page = urllib.request.urlopen(page)
      soup = BeautifulSoup(html_page, "html5lib")
      print("Scraping Page number: " + str(i+1))
      l_main.extend(monster.find_data(soup))
    return(l_main)
      
  # Stores the results in a pandas DataFrame
  def store_results(self, l_main):
    df = pd.DataFrame(l_main)
    df = df[['Date', 'Company', 'Role', 'URL']]
    df=df.dropna()
    df.sort_values(by=['Date'], inplace=True, ascending=False)
    df.to_csv("csv_files/pandas_data.csv", mode='a', header=True, index=False)

  # Clears the CSV file
  def clear_results(self):
    f = open("csv_files/pandas_data.csv", "w")
    f.truncate()
    f.close()

		
if __name__ == '__main__':
  
  display = Display(visible=0, size=(1920, 1080)).start()

  f = open("csv_files/pandas_data.csv", "w")
  f.truncate()
  f.close()

  os.system('clear')

  print('\n')
  print('########################################################')
  print('Monster.ie Job Scraper - Copyright Mariano Vazquez, 2018')
  print('########################################################')
  print('\n')
  
  role = input('Enter role to search: ')

  monster = Monster(role)
  monster.clear_results()

  soup = monster.getPageSource()
  monster.find_data(soup)
  results = monster.iterate_pages()

  monster.store_results(results)
# 	max_pages = int(input('Enter number of pages to search: '))
# 	print('\nScraping list of jobs, please wait...')

# 	l = []
# 	for i in range(max_pages):
# 		page = 'https://www.monster.ie/jobs/search/?q='+query+'&where=Dublin__2C-Dublin&sort=dt.rv.di&page=' + str(i+1)
# 		soup = getPageSource(page)
# 		print("Scraping Page number: " + str(i+1))
# 		l.extend(find_data(soup, l))

# 	df = pd.DataFrame(l)
# 	df = df[['Date', 'Company', 'Role', 'URL']]
# 	df = df.dropna()
# 	df = df.sort_values(by=['Date'], ascending=False)
# 	df.to_csv("csv_files/pandas_data.csv", mode='a', header=True, index=False)

  print("\nDone!!, check the CSV File!")