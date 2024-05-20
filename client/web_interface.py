import time
from api.scraper.delucru_md import ParseDelucru
import streamlit as st
from PIL import Image
from groq import Groq





class WebApp:
    def __init__(self):
        self.client = Groq(
            api_key="API_KEY",
        )
        st.set_page_config(page_title="Plotting Demo", page_icon="📈")
        st.title('CoverLetter AI by Vadim Platon')
        st.subheader('**Generator of letters for job applications**')

        model_options = st.selectbox(
            'Choose job aggregator',
            ['',
             'delucru.md',
             'rabota.md',
             'jobber.md'
             ])
        if model_options == "delucru.md":
            st.header('Delucru.md', divider='red')
            job_url = st.text_input("Paste url to job description page:", placeholder="https://www.delucru.md/job/{id}")
            if job_url:
                parser = ParseDelucru()
                job_data = parser.get_job_by_url(job_url=job_url)
                if job_data is None:
                    st.error("Enter valid URL!")
                    print("Error")
                else:
                    st.success("Success")
                    st.markdown(f'''
                        **Job name:** {parser.job_data['title']}
                        
                        **Salary:** {parser.job_data['salary']}
                        
                        **Schedule:** {parser.job_data['schedule']}
                        
                        **Education:** {parser.job_data['education']}
                        
                        **Experience:** {parser.job_data['exp']}
                        
                        **City:** {parser.job_data['city']}''')

                    desc_on = st.toggle("Toggle job and company description")

                    if desc_on:
                        st.header('Job Description', divider='blue')
                        st.markdown(f"{parser.job_data['job_description']}")
                        st.header('Company Description', divider='blue')
                        st.markdown(f"{parser.job_data['company_description']}")

                    st.header('Cover Letter Personalization', divider='orange')
                    personal_data = {"name": st.text_input("Enter your Name", placeholder="John"),
                                     "surname": st.text_input("Enter your Surname", placeholder="Smith"),
                                     "skills": st.text_area("Enter your skills", placeholder="C++, Python, Java"),
                                     "exp": st.number_input("Enter your Years of Experience", placeholder=2),
                                     }
                    st.json(personal_data)
                    generate_btn = st.button("Generate")
                    if generate_btn:
                        cover_letter = self._generate_cover_letter(personal_data, job_data)
                        st.write_stream(WebApp._stream_data(cover_letter))
        with st.sidebar:
            logo = Image.open('./client/images/logo.png')
            st.image(logo)
            with st.echo():
                st.write("This code will be printed to the sidebar.")

            with st.spinner("Loading..."):
                time.sleep(5)
            st.success("Done!")

    def _generate_cover_letter(self, personal_data, job_data):
        prompt = f'''You ar an AI assistant that writes cover letters for job descriptions.
            Write only cover letter without additional commentaries.
            Here is information about me:
            Name: {personal_data["name"]}
            Surname: {personal_data["surname"]}
            Skills: {personal_data["skills"]}
            Years of experience: {personal_data["exp"]}
            
            Information about company and job position:
            position: {job_data["title"]}
            salary: {job_data["salary"]}
            schedule: {job_data["schedule"]}
            education: {job_data["education"]},
            exp: {job_data["exp"]}
            city: {job_data["city"]}
            company description: {job_data["job_description"]}
            Write a cover letter adapted to me for this job:
            {job_data["job_description"]}'''

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

    @staticmethod
    def _stream_data(data):
        for word in data.split(" "):
            yield word + " "
            time.sleep(0.02)