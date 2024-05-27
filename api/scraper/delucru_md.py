import requests
from bs4 import BeautifulSoup
import re


class ParseDelucru:
    """
    A class for parsing job data from the Delucru.md website.

    Attributes:
        url (str): The URL of the job listing.
        job_data (dict): A dictionary to store job-related information.
    """

    def __init__(self, job_url=None):
        """
        Initializes the ParseDelucru class.

        Args:
            job_url (str, optional): The URL of the job listing. Defaults to None.
        """
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

    def get_job_by_id(self, job_id):
        """
        Retrieves job data based on the job ID.

        Args:
            job_id (int): The unique identifier of the job listing.

        Returns:
            dict: A dictionary containing job-related information.
        """
        self.url = f"https://www.delucru.md/job/{job_id}"
        return self.get_job_by_url(self.url)

    def get_job_by_url(self, job_url=None):
        """
        Retrieves job data based on the provided URL.

        Args:
            job_url (str, optional): The URL of the job listing. Defaults to None.

        Returns:
            dict: A dictionary containing job-related information.
        """
        pattern = r'^https?://(?:www\.)?delucru\.md/job/\d+$'
        job_url = job_url if job_url is not None else self.url
        if re.fullmatch(pattern, job_url) is None:
            return None
        self.url = job_url
        return self._parse_page()

    def _parse_page(self):
        """
        Parses the web page and extracts relevant job data.

        Returns:
            dict: A dictionary containing job-related information.
        """
        page = requests.get(self.url)
        if page.status_code != 200:
            return None
        soup = BeautifulSoup(page.content, "html.parser")
        self.job_data["title"] = soup.title.string.strip()

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
        """
        Returns a string representation of the job data.

        Returns:
            str: A formatted string containing job-related information.
        """
        return str(self.job_data)
