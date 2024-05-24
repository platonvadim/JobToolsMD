import time

from api.AI.custom_groq import GroqClient
from api.scraper.delucru_md import ParseDelucru
from api.scraper.rabota_md import ParseRabota
import streamlit as st
from PIL import Image


class WebApp:
    def __init__(self, api_key):
        self.AI = GroqClient(api_key)
        st.set_page_config(page_title="CoverAI", page_icon="💼")
        st.title('CoverLetter AI by Vadim Platon')
        st.subheader('**Generator of letters for job applications**')

        model_options = st.selectbox(
            'Choose job aggregator',
            ['',
             'delucru.md',
             'rabota.md',
             'custom'
             ])
        if model_options == "delucru.md":
            self._delucru_widget()
        elif model_options == "rabota.md":
            self._rabota_widget()
        elif model_options == "custom":
            self._custom_widget()

        with st.sidebar:
            logo = Image.open('./client/images/logo.png')
            st.image(logo)
            st.markdown("**JobToolsMD** - is a bunch of tools for parsing the information from moldavian jobs"
                        " website and generate cover letters for job application. Powered by Groq.")
            st.header('Instructions', divider='red')
            st.write("Just select job aggregator or custom site,"
                     "paste site URL for parsing, and provide some information about yourself.")

    def _custom_widget(self):
        st.header('Custom', divider='red')
        job_desc = st.text_area("Paste job description:",)
        if job_desc:
            st.success("Success")

            st.header('Cover Letter Personalization', divider='orange')
            personal_data = {"name": st.text_input("Enter your Name", placeholder="John"),
                             "surname": st.text_input("Enter your Surname", placeholder="Smith"),
                             "skills": st.text_area("Enter your skills", placeholder="C++, Python, Java"),
                             "exp": st.number_input("Enter your Years of Experience", placeholder=2),
                             }
            st.json(personal_data)
            col1, col2 = st.columns(2)
            with col1:
                generate_btn = st.button("Generate")
            with col2:
                suitability_btn = st.button("Check suitability")
            if generate_btn:
                cover_letter = self.AI.generate_cover_letter(personal_data, job_desc, by_desc=True)
                st.header('Your Cover Letter', divider='gray')
                st.write_stream(WebApp._stream_data(cover_letter))
            if suitability_btn:
                suitability_response = self.AI.calculate_suitability(personal_data, job_desc, by_desc=True)
                st.header('Your Suitability for this job', divider='gray')
                st.write_stream(WebApp._stream_data(suitability_response))

    def _rabota_widget(self):
        st.header('rabota.md', divider='red')
        job_url = st.text_input("Paste url to job description page:", placeholder="https://www.rabota.md/ro/locuri-de-munca/senior-front-end-razrabotchik-ot-2500/74679")
        if job_url:
            parser = ParseRabota()
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

                desc_on = st.toggle("Toggle job description")

                if desc_on:
                    st.header('Job Description', divider='blue')
                    st.markdown(f"{parser.job_data['job_description']}")

                st.header('Cover Letter Personalization', divider='orange')
                personal_data = {"name": st.text_input("Enter your Name", placeholder="John"),
                                 "surname": st.text_input("Enter your Surname", placeholder="Smith"),
                                 "skills": st.text_area("Enter your skills", placeholder="C++, Python, Java"),
                                 "exp": st.number_input("Enter your Years of Experience", placeholder=2),
                                 }
                st.json(personal_data)
                col1, col2 = st.columns(2)
                with col1:
                    generate_btn = st.button("Generate")
                with col2:
                    suitability_btn = st.button("Check suitability")
                if generate_btn:
                    cover_letter = self.AI.generate_cover_letter(personal_data, job_data)
                    st.header('Your Cover Letter', divider='gray')
                    st.write_stream(WebApp._stream_data(cover_letter))
                if suitability_btn:
                    suitability_response = self.AI.calculate_suitability(personal_data, job_data)
                    st.header('Your Suitability for this job', divider='gray')
                    st.write_stream(WebApp._stream_data(suitability_response))

    def _delucru_widget(self):
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
                col1, col2 = st.columns(2)
                with col1:
                    generate_btn = st.button("Generate")
                with col2:
                    suitability_btn = st.button("Check suitability")
                if generate_btn:
                    cover_letter = self.AI.generate_cover_letter(personal_data, job_data)
                    st.header('Your Cover Letter', divider='gray')
                    st.write_stream(WebApp._stream_data(cover_letter))
                if suitability_btn:
                    suitability_response = self.AI.calculate_suitability(personal_data, job_data)
                    st.header('Your Suitability for this job', divider='gray')
                    st.write_stream(WebApp._stream_data(suitability_response))


    @staticmethod
    def _stream_data(data):
        for word in data.split(" "):
            yield word + " "
            time.sleep(0.02)