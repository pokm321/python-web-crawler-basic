from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
#options.add_experimental_option("detach", True)

search_term = "python"
url = f"https://kr.indeed.com/jobs?q={search_term}"

browser = webdriver.Chrome(options=options)
browser.get(url)

soup = BeautifulSoup(browser.page_source, "html.parser") 
results = []
job_list = soup.find("ul", class_="jobsearch-ResultsList")
jobs = job_list.find_all("li", recursive=False)

for job in jobs:
  zone = job.find("div", class_="mosaic-zone")
  if zone == None:
    anchor = job.select_one("h2 a")
    title = anchor["aria-label"]
    link = anchor["href"]
    company = job.find("span", class_="companyName").string
    location = job.find("div", class_="companyLocation").string
    job_data = {
      'company' : company,
      'location' : location,
      'position' : title,
      'link' : f"https://kr.indeed.com{link}"
    }
    results.append(job_data)

