import requests
from bs4 import BeautifulSoup

def scrape_indeed_job_titles_and_salaries(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    job_titles = []
    salaries = []
    
    # Find all job cards
    for job_card in soup.find_all('div', class_='job_seen_beacon'):
        title = job_card.find('h2', class_='jobTitle').text.strip()
        salary = job_card.find('div', class_='salary-snippet-container')
        if salary:
            salary = salary.text.strip()
        else:
            salary = 'Not listed'
        
        job_titles.append(title)
        salaries.append(salary)

    return list(zip(job_titles, salaries))

# URL for "entry level cybersecurity" jobs on Indeed
url = 'https://www.indeed.com/q-entry-level-cybersecurity-jobs.html'
results = scrape_indeed_job_titles_and_salaries(url)

for title, salary in results:
    print(f"Job Title: {title}, Salary: {salary}")
