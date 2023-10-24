import streamlit as st
import openai
import requests
import pandas as pd
import os
from apikey import OPENAI_API_KEY, FMP_API_KEY

openai.api_key = OPENAI_API_KEY

def get_jsonparsed_data(url):
    response = requests.get(url)
    return response.json()

def get_financial_statements(ticker, limit, period, statement_type):
    if statement_type == "Income Statement":
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    elif statement_type == "Balance Sheet":
        url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    elif statement_type == "Cash Flow":
        url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
    else:
        st.error("Invalid statement type selected. Please choose from Income Statement, Balance Sheet, or Cash Flow.")
        return pd.DataFrame()

    data = get_jsonparsed_data(url)
    if isinstance(data, list) and data:
        return pd.DataFrame(data)
    else:
        st.error("Unable to fetch financial statements. Please ensure the ticker is correct and try again.")
        return pd.DataFrame()

def generate_financial_summary(financial_statements, statement_type):
    summaries = []
    for i in range(len(financial_statements)):
        summary = f"For the period ending {financial_statements['date'][i]}, the company reported the following: ..."
        summaries.append(summary)
    
    all_summaries = "\n\n".join(summaries)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI trained to provide financial analysis based on financial statements."},
            {"role": "user", "content": f"Please analyze the following data and provide insights:\n{all_summaries}.\n Write each section out as instructed in the summary section and then provide analysis of how it's changed over the time period in a manner that is easy to understand for the average layman."}
        ]
    )
    return response['choices'][0]['message']['content']

def financial_statements():
    st.title('GPT-4 & Financial Statements')
    statement_type = st.selectbox("Select financial statement type:", ["Income Statement", "Balance Sheet", "Cash Flow"])
    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox("Select period:", ["Annual", "Quarterly"]).lower()
    with col2:
        limit = st.number_input("Number of past financial statements to analyze:", min_value=1, max_value=10, value=4)
    ticker = st.text_input("Please enter the company ticker:")
    if st.button('Run'):
        if ticker:
            ticker = ticker.upper()
            financial_statements = get_financial_statements(ticker, limit, period, statement_type)
            with st.expander("View Financial Statements"):
                st.dataframe(financial_statements)
            financial_summary = generate_financial_summary(financial_statements, statement_type)
            st.write(f'Summary for {ticker}:\n {financial_summary}\n')

def main():
    st.sidebar.title('AI Financial Analyst')
    app_mode = st.sidebar.selectbox("Choose your AI assistant:", ["Financial Statements"])
    if app_mode == 'Financial Statements':
        financial_statements()

if __name__ == '__main__':
    main()
