import streamlit as st
import openai
import requests
import os
from apikey import OPENAI_API_KEY, FMP_API_KEY

openai.api_key = OPENAI_API_KEY

def get_financial_statements(ticker, limit, period, statement_type):
    # ... (code for fetching financial statements)

def generate_financial_summary(financial_statements, statement_type):
    # ... (code for generating summary using GPT-4)

def financial_statements():
    # ... (Streamlit UI code)

def main():
    st.sidebar.title('AI Financial Analyst')
    app_mode = st.sidebar.selectbox("Choose your AI assistant:", ["Financial Statements"])
    if app_mode == 'Financial Statements':
        financial_statements()

if __name__ == '__main__':
    main()
