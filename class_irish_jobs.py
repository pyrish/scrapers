#!/usr/bin/python3
import pandas as pd
import os
from datetime import datetime
from bs4 import BeautifulSoup
import urllib.request


class IrishJobs(object):
  def __init__(self, role):
        self.role = role
        self.url = 'https://www.irishjobs.ie/ShowResults.aspx?Keywords={}&Location=102&Category=3&Recruiter=All&SortBy=MostRecent&PerPage=100'.format(role)
  
  # Makes the soup
  def getPageSource(self):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}
    req = urllib.request.Request(self.url, headers=hdr)
    page = urllib.request.urlopen(req)
    soup = BeautifulSoup(page, "html5lib")
    return(soup)
			
	# Finds the data according to the search term provided
  def find_data(self, soup):
    base_url = 'https://www.irishjobs.ie/'
    l_main = []
    for a in soup.find_all(attrs={"itemtype" : "https://schema.org/JobPosting"}):
      d = {}
      job_info = a.find('h2').find('a')
      d["Company"] = a.find('h3').find('a').get_text()
      url = job_info['href']
      d["URL"] = (base_url + url)
      d["Role"] = (job_info.get_text())
      d["Date"] = a.find('li',class_='updated-time').get_text().replace('Updated','').strip()
      d["Date"] = pd.to_datetime(d["Date"], format='%d/%m/%Y')
      l_main.append(d)
    return l_main

       # Store the results in a pandas DataFrame
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
  
  f = open("csv_files/pandas_data.csv", "w")
  f.truncate()
  f.close()

  os.system('clear')
	
  print('\n')
  print('##########################################################')
  print('IrishJobs.ie Job Scraper - Copyright Mariano Vazquez, 2018')
  print('##########################################################')
  print('\n')

  role = input('Enter role to search: ')

  irish_jobs = IrishJobs(role)
  irish_jobs.clear_results()
  soup = irish_jobs.getPageSource()

  results_list = irish_jobs.find_data(soup)
  irish_jobs.store_results(results_list)

  print("\nDone!!, check the CSV File!")