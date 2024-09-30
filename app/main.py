import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from portfolio import Portfolio
from utils import clean_text
from chains import Chain


def create_streamlit_app(llm,portfolio,clean_text):
    st.title('Cold Email Generator')
    url_input=st.text_input('Enter the url :',value='https://www.google.com/about/careers/applications/jobs/results/88533478290662086-software-development-manager-generative-ai-google-workspace')
    submit_btn=st.button("Submit")

    if submit_btn:
        try:
            loader = WebBaseLoader([url_input])
            data=clean_text(loader.load().pop().page_content)
            print(data)
            portfolio.load_portfolio()
            jobs=llm.extract_jobs(data)
            for job in jobs:
                skills=job.get('skills',[])
                links=portfolio.query_links(skills)
                email=llm.write_email(job,links)
                st.code(email,language='markdown')
        except Exception as e:
            st.error(f'An error has occured :{e}')


if __name__=='__main__':
    chain=Chain()
    portfolio=Portfolio()
    st.set_page_config(layout="wide",page_title='Cold Email generator',page_icon='📧')
    create_streamlit_app(chain,portfolio,clean_text)