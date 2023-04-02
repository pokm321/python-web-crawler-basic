from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs

keyword = input("What do you want to search for?")

print("Searching on WWR...")
wwr = extract_wwr_jobs(keyword)
print(len(wwr), "jobs found on WWR.")

print("Searching on Indeed...")
indeed = extract_indeed_jobs(keyword)
print(len(indeed), "jobs found on Indeed.")

jobs = wwr + indeed
print(len(jobs), "jobs found in total.")

file = open(f"{keyword}.csv", "w")
file.write("Position,Company,Location,URL\n")
for job in jobs:
    file.write(f"\"{job['position']}\",\"{job['company']}\",\"{job['location']}\",\"{job['link']}\"\n")
file.close()