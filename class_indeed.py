# -*- coding: utf-8 -*-
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.common.exceptions import TimeoutException

#from pyvirtualdisplay import Display

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import os

class IndeedScraper(object):
    def __init__(self, role):
        self.role = role
        self.url = 'https://ie.indeed.com/jobs?q={}&l=Dublin&sort=date&limit=20&fromage=3&radius=25&start=0'.format(role)
        #self.driver = webdriver.Firefox()
        #self.delay = 3

#     def load_indeed_url(self):
#         self.driver.get(self.url)
#         try:
#             wait = WebDriverWait(self.driver, self.delay)
#             wait.until(EC.presence_of_element_located((By.CLASS_NAME, "input_text")))
#             print("Page is ready")
#         except TimeoutException:
#             print("Loading took too much time")
            
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

      
    def find_info(self, source):
      l = []
      html_page = urllib.request.urlopen(self.url)
      source = BeautifulSoup(html_page, "html5lib")
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

  #display = Display(visible=0, size=(1920, 1080)).start()
  
  role = str(input("Enter role to search: "))
  
  scraper = IndeedScraper(role) 
  pages = scraper.find_pages()
  print('# {} pages were found from the past 3 days'.format(len(pages)))
  max_pages = int(input('# Enter number of pages to scrape: '))
  print('\n')
  
  l_main = []
  cont = 1
  # Iterate through the pages
  for i in pages[:max_pages]:
    html_page = urllib.request.urlopen(i)
    source = BeautifulSoup(html_page, "html5lib")
    print("Scraping Page number: " + str(cont))
    results = scraper.find_info(source)
    cont +=1
    l_main.extend(results)
 
   # Put all results into a DataFrame
  df = pd.DataFrame(l_main)
  df = df[['Date', 'Company', 'Role', 'URL']]
  df=df.dropna()
  df.sort_values(by=['Date'], inplace=True, ascending=False)
  df.to_csv("csv_files/pandas_data.csv", mode='a', header=True, index=False)

  print("\nDone!!, check the CSV File!")