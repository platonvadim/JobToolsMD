import requests
from bs4 import BeautifulSoup


class ParseDelucru:
    def __init__(self, job_url: str = None):
        self.url = job_url
        self.job_data = {
            "title": "",
            "salary": "",
            "schedule": "",
            "education": "",
            "exp": "",
            "city": "",
            "job_description": "",
            "company_description": "",
        }
        self.get_job_by_url(job_url)

    def get_job_by_id(self, job_id):
        self.url = f"https://www.delucru.md/job/{job_id}"
        return self._parse_page()

    def get_job_by_url(self, job_url):
        self.url = job_url
        return self._parse_page()

    def _parse_page(self):
        page = requests.get(self.url)
        if page.status_code != 200:
            return None
        soup = BeautifulSoup(page.content, "html.parser")
        self.job_data["title"] = soup.title.string

        lead_data = soup.findAll('div', class_="lead")[0]

        job_summary = lead_data.findAll('div', class_="col mb-4")

        for job_item in job_summary:
            description = job_item.find("div", "text-muted3").string
            value = job_item.find("div", "lead-item").getText().strip()

            match description:
                case "Salariu:":
                    self.job_data['salary'] = value
                case "Program de lucru:":
                    self.job_data['schedule'] = value
                case "Studii:":
                    self.job_data['education'] = value
                case "Experiență:":
                    self.job_data['exp'] = value
                case "Oraș:":
                    self.job_data['city'] = value

        self.job_data["job_description"] = soup.find(id="job-description").getText()
        company_description = soup.find(id="about")
        company_description.h3.decompose()
        self.job_data["company_description"] = company_description.getText().strip()
        return self.job_data

    def __str__(self):
        return str(self.job_data)




