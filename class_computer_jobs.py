#!/usr/bin/python3
# -*- coding: utf-8 -*-

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


class Computer(object):
  def __init__(self, role):
        self.role = role
        self.url = 'https://www.computerjobs.ie/jobboard/cands/JobResults.asp?c=1&strKeywords={}&lstPostedDate=3&lstRegion=Central+Dublin&lstRegion=South+Dublin&lstRegion=North+Dublin&lstRegion=West+Dublin&pg=1'.format(role)
        
  def getPageSource(self, url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib.request.Request(url, headers=hdr)
    html_page = urllib.request.urlopen(req)
    soup = BeautifulSoup(html_page, "html5lib")
    return(soup)

  def get_number_pages(self):
    soup = computer.getPageSource(self.url)
    num_results = soup.find("strong").contents
    makeitastring = ''.join(map(str, num_results))
    temp = (int(makeitastring)) / 10
    page_no = math.ceil(temp)
    return(page_no)

  def find_data(self, soup):
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
  
  def iterate_pages(self, no_pages):
    l_main = []
    for i in range(no_pages):
      page = self.url[:-1] + str(i+1)
      soup = computer.getPageSource(page)
      print("Scraping Page number: " + str(i+1))
      l_main.extend(computer.find_data(soup))
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

  os.system('clear')

  print('\n')
  print('#############################################################')
  print('Computerjobs.ie Job Scraper - Copyright Mariano Vazquez, 2018')
  print('#############################################################')
  print('\n')

  role = input('Enter role to search: ')
  print('\nLooking for Jobs, please wait...')
  print('\n')
  computer = Computer(role)
  
  computer.clear_results()
  
  no_pages = computer.get_number_pages()
  results = computer.iterate_pages(no_pages)
  computer.store_results(results)
  


  print("\nDone!!, check the CSV File!")