import requests
from bs4 import BeautifulSoup
import re


class ParseRabota:
    def __init__(self, job_url=None):
        self.url = job_url
        self.job_data = {
            "title": "",
            "salary": "",
            "schedule": "",
            "education": "",
            "exp": "",
            "city": "",
            "job_description": "",
        }
        # self.get_job_by_url(job_url)

    def get_job_by_id(self, job_id):
        self.url = f"https://www.delucru.md/job/{job_id}"
        return self.get_job_by_url(self.url)

    def get_job_by_url(self, job_url=None):
        pattern = r"^https?://(?:www\.)?rabota\.md/.+?(\d+)/?$"
        # match = re.search(pattern, job_url)
        # if not match:
        #     return None
        # job_id = match.group(1)
        job_url = job_url if job_url is not None else self.url
        if re.fullmatch(pattern, job_url) is None:
            return None
        self.url = job_url
        return self._parse_page()

    def _parse_page(self):
        page = requests.get(self.url)
        if page.status_code != 200:
            return None
        soup = BeautifulSoup(page.content, "html.parser")
        self.job_data["title"] = soup.title.string.strip()

        self.job_data["job_description"] = soup.findAll('div', class_="vacancy-content")[0].getText()

        # job_summary = lead_data.findAll('div', class_="vacancy-content")

        # job_details = {}
        # for item in soup.find_all("div", class_="lead-item"):
        #     label = item.find("div", class_="text-muted3").get_text().strip()
        #     value = item.get_text().replace(label, "").strip()
        #     job_details[label] = value
        return self.job_data

    def __str__(self):
        return str(self.job_data)




