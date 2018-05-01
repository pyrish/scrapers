# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import os

class IndeedScraper(object):
    def __init__(self, role):
        self.role = role
        self.url = 'https://ie.indeed.com/jobs?q={}&l=Dublin&sort=date&limit=20&fromage=3&radius=25&start=0'.format(role)
 

    # Find number of pages given the term provided       
    def find_pages(self):
        pages = []
        html_page = urllib.request.urlopen(self.url)
        source = BeautifulSoup(html_page, "html5lib")
        base_url = 'https://ie.indeed.com'
        for a in source.find_all('div', class_= 'pagination'):
          for link in a.find_all('a', href=True):
            pages.append(base_url + link['href'])
        pages.insert(0, base_url + '/jobs?q={}&l=Dublin&sort=date&limit=20&fromage=3&radius=25&start=0'.format(self.role))
        pages.pop()
        return pages

    # Scrape each page to pull the Company, Role, URL and Date  
    def find_info(self, source):
      l = []
      for info in source.find_all("td",  {"id": "resultsCol"}):
        for div in info.find_all('div', {"class": ["row", "result", "clickcard"]}):
          d = {}
          try:
            link = div.find('h2', class_= 'jobtitle').find('a')
            role = link.get_text()
            d["Company"] = div.find('span', class_= 'company').get_text().strip()
            d["Role"] = role
            d["URL"] = 'http://www.indeed.com' + link['href']
            d["Date"] = div.find('span', class_= 'date').get_text().strip()
            l.append(d)
          except:
            pass
      return l
    
    # Iterate through the pages
    def iterate_pages(self, pages, max_pages):
      l_main = []
      cont = 1
      for i in pages[:max_pages]:
        html_page = urllib.request.urlopen(i)
        source = BeautifulSoup(html_page, "html5lib")
        print("Scraping Page number: " + str(cont))
        results = scraper.find_info(source)
        cont +=1
        l_main.extend(results)
      return(l_main)
    
    # Store the results in a pandas DataFrame
    def store_results(self, l_main):
      df = pd.DataFrame(l_main)
      df = df[['Date', 'Company', 'Role', 'URL']]
      df=df.dropna()
      df.sort_values(by=['Date'], inplace=True, ascending=False)
      df.to_csv("csv_files/pandas_data.csv", mode='a', header=True, index=False)
      
    
if __name__ == '__main__':
  
  f = open("csv_files/pandas_data.csv", "w")
  f.truncate()
  f.close()

  os.system('clear')

  print('\n')
  print('###############################################################')
  print('Indeed.ie CLASS!! Job Scraper - Copyright Mariano Vazquez, 2018')
  print('###############################################################')
  print('\n')

  role = str(input("Enter role to search: "))
  
  scraper = IndeedScraper(role) 
  pages = scraper.find_pages()
  print('# {} pages were found from the past 3 days'.format(len(pages)))
  max_pages = int(input('# Enter number of pages to scrape: '))
  print('\n')
  
  results_list = scraper.iterate_pages(pages, max_pages)
  scraper.store_results(results_list)

  print("\nDone!!, check the CSV File!")