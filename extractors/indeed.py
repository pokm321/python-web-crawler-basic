from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_page_count(keyword):
  options = Options()
  options.add_argument("--no-sandbox")
  options.add_argument("--disable-dev-shm-usage")
  #options.add_experimental_option("detach", True)

  url = f"https://kr.indeed.com/jobs?q={keyword}"

  browser = webdriver.Chrome(options=options)
  browser.get(url)

  soup = BeautifulSoup(browser.page_source, "html.parser") 
  pagination = len(soup.find("nav", attrs={"aria-label": "pagination"}).find_all("div", recursive=False))
  if pagination <= 1:
    return 1
  else:
    return pagination - 1

def extract_indeed_jobs(keyword):
  results = []
  pages = get_page_count(keyword)

  for page in range(pages):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_experimental_option("detach", True)

    url = f"https://kr.indeed.com/jobs?q={keyword}&start={page * 10}"

    browser = webdriver.Chrome(options=options)
    browser.get(url)

    soup = BeautifulSoup(browser.page_source, "html.parser") 

    job_list = soup.find("ul", class_="jobsearch-ResultsList")
    jobs = job_list.find_all("li", recursive=False)

    for job in jobs:
      zone = job.find("div", class_="mosaic-zone")
      if zone == None:
        anchor = job.select_one("h2 a")
        title = anchor["aria-label"].replace(",", " ")
        link = anchor["href"].replace(",", " ")
        company = job.find("span", class_="companyName").string.replace(",", " ")
        location = job.find("div", class_="companyLocation").string.replace(",", " ")
        job_data = {
          'company' : company,
          'location' : location,
          'position' : title,
          'link' : f"https://kr.indeed.com{link}"
        }
        results.append(job_data)
  return results