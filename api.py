import streamlit as st
from openai import OpenAI
import urllib, urllib.request
from urllib.request import urlopen
import feedparser
st.set_page_config(page_title="Research Summarise Page", page_icon="🧠", layout="centered", )
st.header("Enter your text and get the summary of the research paper")

class setting_page_config():
    def __init__(self):
        self.user_text_input = st.text_input(label="Please enter your text here ")
        self.user_page_number = st.slider("Selec the number of results" , min_value= 1, max_value=10, value=2, step=1)
        self.submitted_button = st.button("Submit", )
    

    def expander(d):

        with st.expander(d["title"]):
            st.write(d["id"])
            st.write(d["published"][:10])
            st.write(d["summary"])
 
class xml_data_requests(setting_page_config):

    def __init__(self):
        super().__init__()
    
    def format_user_input(self):
        self.user_text_input.strip()
        self.user_text_input = self.user_text_input.replace(" ", "%20")
        return self.user_text_input
        
    def get_data(self):
        user_formatted_input = self.format_user_input()
        url = f'http://export.arxiv.org/api/query?search_query=all:{user_formatted_input}&start=0&max_results={self.user_page_number}'
        response = urlopen(url)
        entries =   feedparser.parse(response)
        return entries
    
    def main(self):
        if self.submitted_button:

          entries = self.get_data()
          for x in range(0, self.user_page_number):
              dict = {
                  "title": entries.entries[x].title,
                  "id": entries.entries[x].id,
                  "published": entries.entries[x].published,
                  "summary": entries.entries[x].summary
              }
              setting_page_config.expander(dict)
        

xml_data_requests().main()