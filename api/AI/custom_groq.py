from groq import Groq


class GroqClient:
    def __init__(self, api):
        self.client = Groq(
                api_key=api,
            )

    def generate_cover_letter(self, personal_data, job_data, by_desc=False):
        if by_desc:
            details = job_data
        else:
            details = f'''
            position: {job_data["title"]}
            salary: {job_data["salary"]}
            schedule: {job_data["schedule"]}
            education: {job_data["education"]},
            exp: {job_data["exp"]}
            city: {job_data["city"]}
            company description: {job_data["job_description"]}
            Write a cover letter adapted to me for this job:
            {job_data["job_description"]}'''

        prompt = f'''You ar an AI assistant that writes cover letters for job descriptions.
            Write only cover letter without additional commentaries.
            Here is information about me:
            Name: {personal_data["name"]}
            Surname: {personal_data["surname"]}
            Skills: {personal_data["skills"]}
            Years of experience: {personal_data["exp"]}
    
            Information about company and job position:
            {details}

            The response will contain only cover letter!'''

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        return chat_completion.choices[0].message.content

    def calculate_suitability(self, personal_data, job_data, by_desc):
        if by_desc:
            details = job_data
        else:
            details = f'''
            position: {job_data["title"]}
            salary: {job_data["salary"]}
            schedule: {job_data["schedule"]}
            education: {job_data["education"]},
            exp: {job_data["exp"]}
            city: {job_data["city"]}
            company description: {job_data["job_description"]}
            Job Description: 
            {job_data["job_description"]}'''

        prompt = f'''You ar an AI HR manager that calculates in percents
            how work is suitable for me based on my info and job description.

            Here is information about me:
            Name: {personal_data["name"]}
            Surname: {personal_data["surname"]}
            Skills: {personal_data["skills"]}
            Years of experience: {personal_data["exp"]}

            Information about company and job position:
            {details}
            '''

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
        )

        return chat_completion.choices[0].message.content
