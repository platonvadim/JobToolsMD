import requests
from bs4 import BeautifulSoup
import re


class ParseRabota:
    """
        A class for parsing job data from the Rabota.md website.

        Attributes:
            url (str): The URL of the job listing.
            job_data (dict): A dictionary to store job-related information.
    """

    def __init__(self, job_url=None):
        """
        Initializes the ParseRabota class.

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
        }
        # self.get_job_by_url(job_url)

    def get_job_by_id(self, job_id):
        """
        Retrieves job data based on the job ID.

        Args:
            job_id (int): The unique identifier of the job listing.

        Returns:
            dict: A dictionary containing job-related information.
        """
        self.url = f"https://www.rabota.md/ro/locuri-de-munca/{job_id}"
        return self.get_job_by_url(self.url)

    def get_job_by_url(self, job_url=None):
        """
        Retrieves job data based on the provided URL.

        Args:
            job_url (str, optional): The URL of the job listing. Defaults to None.

        Returns:
            dict: A dictionary containing job-related information.
        """
        pattern = r"^https?://(?:www\.)?rabota\.md/.+?(\d+)/?$"
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

        self.job_data["job_description"] = soup.findAll('div', class_="vacancy-content")[0].getText()

        return self.job_data

    def __str__(self):
        """
        Returns a string representation of the job data.

        Returns:
            str: A formatted string containing job-related information.
        """
        return str(self.job_data)
