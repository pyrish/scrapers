# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib.request
import math
import pandas as pd
import os

from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Indeed.ie Scraper
class IndeedScraper(object):
    def __init__(self, role):
        self.role = role
        self.url = 'https://ie.indeed.com/jobs?as_and={}&radius=25&l=Dublin&fromage=3&limit=10&sort=date&start=0'.format(role)
 
    # Finds number of pages given the term provided       
    def find_pages(self):
        pages = []
        html_page = urllib.request.urlopen(self.url)
        source = BeautifulSoup(html_page, "html5lib")
        base_url = 'https://ie.indeed.com'
        for a in source.find_all('div', class_= 'pagination'):
          for link in a.find_all('a', href=True):
            pages.append(base_url + link['href'])
        pages.insert(0, base_url + '/jobs?as_and={}&radius=25&l=Dublin&fromage=3&limit=10&sort=date&start=0'.format(self.role))
        pages.pop()
        return pages

    # Scrapes each page to pull the Company, Role, URL and Date  
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
    
    # Iterates through the pages
    def iterate_pages(self, pages, max_pages):
      l_main = []
      cont = 1
      for i in pages[:max_pages]:
        html_page = urllib.request.urlopen(i)
        source = BeautifulSoup(html_page, "html5lib")
        print("Scraping Page number: " + str(cont))
        results = indeed.find_info(source)
        cont +=1
        l_main.extend(results)
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

      
# Irish Jobs Scraper      
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
    max_pages = int(input('\nEnter number of pages to search: '))
    print('\n>>> Scraping list of jobs, please wait...')
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

# Computer Jobs Scraper class
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
  running = True
  
  while running:

    print('\n')
    print('###############################################################')
    print('         Job Scraper - Copyright Mariano Vazquez, 2018'         )
    print('###############################################################')
    print('\n')
    
    print('1) Indeed        4) Computer Jobs')
    print('2) IrishJobs     5) All of them')
    print('3) Monster       6) Quit')

    choice = str(input("\nMake your choice: "))
    
    if choice == '1':

      role = str(input("\nEnter role to search: "))

      indeed = IndeedScraper(role)
      indeed.clear_results()
      
      pages = indeed.find_pages()
      print('# {} pages were found from the past 3 days'.format(len(pages)))
      max_pages = int(input('# Enter number of pages to scrape: '))
      print('\n')

      results_list = indeed.iterate_pages(pages, max_pages)
      indeed.store_results(results_list)
      os.system('clear')
    
    elif choice == '2':
      
      role = input('\nEnter role to search: ')
      print('\n>>> Searching jobs, please wait..')

      irish_jobs = IrishJobs(role)
      irish_jobs.clear_results()
      soup = irish_jobs.getPageSource()

      results_list = irish_jobs.find_data(soup)
      irish_jobs.store_results(results_list)
      os.system('clear')
      
    elif choice == '3':
      
      role = input('\nEnter role to search: ')
      print('\n>>> Gathering results, please wait...')
      
      monster = Monster(role)
      monster.clear_results()

      soup = monster.getPageSource()
      monster.find_data(soup)
      results = monster.iterate_pages()

      monster.store_results(results)
      os.system('clear')
    
    elif choice == '4':
      
      role = input('\nEnter role to search: ')
      print('\n>>> Gathering results, please wait...')
      print('')
      
      computer = Computer(role)
      computer.clear_results()

      no_pages = computer.get_number_pages()
      results = computer.iterate_pages(no_pages)
      computer.store_results(results)
      os.system('clear')
    
    elif choice == '6':
      running = False
  print('\nProgram ending... Bye!')