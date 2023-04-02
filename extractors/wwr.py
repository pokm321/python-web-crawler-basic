from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
  url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
  response = get(url)

  if response.status_code != 200:
    print("Error")
  else:
    results = []
    soup = BeautifulSoup(response.text, "html.parser")
    job_sections = soup.find_all('section', class_="jobs")
    for job_section in job_sections:
      job_posts = job_section.find_all('li')
      job_posts.pop(-1)

      for post in job_posts:
        anchor = post.find_all('a')[1]
        link = anchor['href']
        company, kind, location = anchor.find_all('span', class_='company')
        title = anchor.find('span', class_='title')
        job_data = {
          'company' : company.string.replace(",", " "),
          'kind' : kind.string.replace(",", " "),
          'location' : location.string.replace(",", " "),
          'position' : title.string.replace(",", " "),
          'link' : f"https://weworkremotely.com{link}"
        }
        results.append(job_data)
    return results
