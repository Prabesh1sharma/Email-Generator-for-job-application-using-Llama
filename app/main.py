import streamlit as st 
from langchain_community.document_loaders import WebBaseLoader


from chain import Chain
from portfolio import Portfolio
from utilis import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title(" 📧 Mail Generator")
    url_input = st.text_input("Enter a url :",value="https://jobs.nike.com/job/R-38652?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skils = job.get('skills',[])
                links = portfolio.query_links(skils)
                email = llm.write_email(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An error occured: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Mail Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)


