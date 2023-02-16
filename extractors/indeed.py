from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_page_count(keyword):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  
  browser = webdriver.Chrome(options=options)
  
  base_url = f"https://www.indeed.com/jobs?q={keyword}&l=San+Francisco"
  browser.get(base_url)
  soup = BeautifulSoup(browser.page_source, "html.parser")
  pagination = soup.find("nav", class_="ecydgvn0")
  if pagination == None:
    return 1
  pages = pagination.find_all("div", class_="ecydgvn1")
  count = len(pages)
  if count >= 5:
    return 5
  elif count==0:
    return 1
  else:
    return count

def extract_indeed_jobs(keyword): 
  pages = get_page_count(keyword)
  results = []
  for page in range(pages):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    browser = webdriver.Chrome(options=options)
    
    base_url = f"https://www.indeed.com/jobs?q={keyword}&start={page*10}"
    browser.get(base_url)
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
    jobs_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = jobs_list.find_all('li', recursive=False)
    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor['aria-label']
        link = anchor['href']
        company = job.find("span", class_="companyName")
        location = job.find("div", class_="companyLocation")
        job_data = {
          'link':f"https://www.indeed.com{link}",
          'company': company.string,
          'location': location.string,
          'position':title,
        }
        for each in job_data:
          if job_data[each] != None:
            job_data[each] = job_data[each].replace(",", " ")
        results.append(job_data)
  return results