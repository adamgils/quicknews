import requests
from bs4 import BeautifulSoup
import openai
import streamlit as st

# UI Text

"""
# QuickNews: _News & Article Summarizer_
"""
st.markdown("Welcome to QuickNews, the fastest way to summarize articles and news reports!")
# Set the URL that you want to make a request to.
article_url = st.text_input("_Enter an article's URL:_")
st.markdown("_Created by [Adam Gilani](https://twitter.com/adamgilani)_")

# Feeds API Key From StreamLit "Secrets"
openai.api_key = st.secrets["API_KEY"]

def summarize():
    # State starting text variable with GPT prompt.
    text = "Summarize this information in 400 characters: "
    
    # Make the request and store the response.
    response = requests.get(article_url)
    
    # Parse the HTML content of the website.
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract the text from the website and print it.
    for p in soup.find_all("p"):
      text += p.text

    # Calculate estimated token count for request.
    estimated_tokens = len(text) / 5.1
    
    if estimated_tokens <= 3500:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            temperature=1,
            max_tokens=500
        )
        return response["choices"][0]["text"]
    else:
        return "Article too long... try another article!"


if article_url:
    # Text generation spinner
    with st.spinner("Please wait while your summary is being generated..."):
        # Generate the summarization text
        summary = summarize()

    # Feed the summarization text to the app
    st.write(summary)
