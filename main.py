from requests import get
from bs4 import BeautifulSoup

base_url = "https://weworkremotely.com/remote-jobs/search?term="
search_term = "python"

response = get(f"{base_url}{search_term}")

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
      company, kind, region = anchor.find_all('span', class_='company')
      title = anchor.find('span', class_='title').string.encode('utf-8')
      job_data = {
        'company' : company.string,
        'kind' : kind.string,
        'region' : region.string,
        'position' : str(title).lstrip('b').strip('\''),
        'link' : link
      }
      results.append(job_data)
  for result in results:
    print(result)
    print("-----------------------------------------------------")

  print(type(soup))