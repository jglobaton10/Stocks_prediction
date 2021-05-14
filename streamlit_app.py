
import pandas as pd
import yfinance as yf
import streamlit as st
import requests as rq
from datetime import timedelta, date
import time 


# Tickers
tickers_list = 'https://raw.githubusercontent.com/shilewenuw/get_all_tickers/master/get_all_tickers/tickers.csv'
tickers = pd.read_csv(tickers_list, header = None)
# These tickers were not included in the filed  so it was necessary to add them manually
tickers = tickers.append({0:'GOOGL' },ignore_index=True)
tickers = tickers.append({0:'AMZN' },ignore_index=True)
tickers = tickers.append({0:'AAPL' },ignore_index=True)
tickers = tickers.append({0:'FB' },ignore_index=True)
# Header of the app 
#st.write(' # **Stock Prediction App - V1**')
st.markdown("<h1 style='text-align: left; color: #fece7b; '>Stock Prediction App - V1 </h1>", unsafe_allow_html=True)



# First 100 stocks with the highers Price
st.write('**Trendig stocks**')

# Top 100 stocks info  - we only download the info about the first 20 
top_100_stocks = pd.read_html('https://stock-screener.org/top-100-stocks.aspx')[2].Symbol.to_list()[:20]
# Info of the seven las days 
start_date = date.today()   
top_100_stocks_data = yf.download(' '.join(top_100_stocks), group_by = 'column', end=start_date.strftime('%Y-%m-%d'), 
                                  start= (start_date - timedelta(days=7)).strftime('%Y-%m-%d'), period = '1d')

# Prices of the stocks in the previous time period
top_100_stocks_data_previous = yf.download(' '.join(top_100_stocks), group_by = 'column', end=(start_date - timedelta(days=7)).strftime('%Y-%m-%d'), 
                                  start= (start_date - timedelta(days=14)).strftime('%Y-%m-%d'), period = '1d')


# Functions to apply conditional formatting to the cells in the DataFrame -----------------------------------------------------------------------------------
def select_col_Close(x):
    c1 = 'color: #f63467'
    c2 = 'color: #d5fe7b' 
    #compare columns
    mask = pd.DataFrame(top_100_stocks_data.Close.median() - top_100_stocks_data_previous.Close.median()) > 0 
    #DataFrame with same index and columns names as original filled empty strings
    df1 =  pd.DataFrame(c2, index=x.index, columns=x.columns)
    #modify values of df1 column by boolean mask
    df1.loc[mask[0], 'Current'] = c1
    #print(df1.columns)
    df1 = df1.drop(0,axis= 1)
    df1 = df1.fillna(c2)
    df1[0] = df1['Current']
    df1 = df1.drop('Current',axis = 1)
 
    return df1
def select_col_High(x):
    c1 = 'color: #f63467'
    c2 = 'color: #d5fe7b' 
    #compare columns
    mask = pd.DataFrame(top_100_stocks_data.High.median() - top_100_stocks_data_previous.High.median()) > 0 
    #DataFrame with same index and columns names as original filled empty strings
    df1 =  pd.DataFrame(c2, index=x.index, columns=x.columns)
    #modify values of df1 column by boolean mask
    df1.loc[mask[0], 'Current'] = c1
    #print(df1.columns)
    df1 = df1.drop(0,axis= 1)
    df1 = df1.fillna(c2)
    df1[0] = df1['Current']
    df1 = df1.drop('Current',axis = 1)
 
    return df1
def select_col_Low(x):
    c1 = 'color: #f63467'
    c2 = 'color: #d5fe7b' 
    #compare columns
    mask = pd.DataFrame(top_100_stocks_data.Low.median() - top_100_stocks_data_previous.Low.median()) < 0 
    #DataFrame with same index and columns names as original filled empty strings
    df1 =  pd.DataFrame(c2, index=x.index, columns=x.columns)
    #modify values of df1 column by boolean mask
    df1.loc[mask[0], 'Current'] = c1
    #print(df1.columns)
    df1 = df1.drop(0,axis= 1)
    df1 = df1.fillna(c2)
    df1[0] = df1['Current']
    df1 = df1.drop('Current',axis = 1)
 
    return df1
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Writing the dataframes
col1_stocks_close, col2_stocks_close,col3_stocks_close = st.beta_columns(3)
col1_stocks_close.write('Close Price')
col1_stocks_close.dataframe(pd.DataFrame(top_100_stocks_data.Close.median().sort_values(ascending = False )).style.apply(select_col_Close, axis=None))
col2_stocks_close.write('High Price')
col2_stocks_close.write( pd.DataFrame(top_100_stocks_data.High.median().sort_values(ascending = False )).style.apply(select_col_High, axis=None)         )
col3_stocks_close.write('Low Price')
col3_stocks_close.write( pd.DataFrame(top_100_stocks_data.Low.median().sort_values(ascending = False )).style.apply(select_col_Low, axis=None))

## Selection menu of the companies names 
st.write('## **Companies**')

#
# Returns the parameters related with the dates and  companies the user wants to consult
#
def graph_values() -> tuple:

  selections = st.multiselect('Companies', tickers[0])  
  ## Date selectors 
  col1_date_initial, col2_date_final = st.beta_columns(2)
  col1_date_initial.write(' ## **Initial Date**')
  date_initial = col1_date_initial.date_input('Select the day from you want to consult the stocks')
  col2_date_final.write('## **Final Date**')
  date_final = col2_date_final.date_input('Select the day untill you want to consult the stocks')
  return (selections,date_initial,date_final)


selections, date_initial, date_final = graph_values()

try:
  
  # Stocks data
  stocks_data = yf.download(' '.join(selections), group_by = 'column', start=date_initial, end= date_final, period = '1d')
  # Stocks pricing graph
  
  col1_stocks_High, col2_stocks_Low = st.beta_columns(2)
  # High
  col1_stocks_High.write('## **Highest value of the stocks**')
  col1_stocks_High.line_chart(stocks_data.High)
  # Low
  col2_stocks_Low.write('## **Lowest value of the stocks**')
  col2_stocks_Low.line_chart(stocks_data.Low)
  # Close
  st.write('## **Close value of the stocks**')
  st.line_chart(stocks_data.Close)
except Exception as e:
  st.markdown("<h1 style='text-align: center; color: #f63467; padding-top: 100px;padding-bottom: 100px'>Please select the stocks to start </h1>", unsafe_allow_html=True)

# Stocks Prices Prediction -----------------------------------------------------------------------------------------------------------------------
st.write('## **Stock Prices Prediction**')
selections_for_prediction = st.multiselect('Copanies for Predictions', tickers[0])  
#start_date = date.today()   
#data_for_predictions = yf.download(' '.join(top_100_stocks), group_by = 'column', end=start_date.strftime('%Y-%m-%d'), 
#                                  start= (start_date - timedelta(days=1400)).strftime('%Y-%m-%d'), period = '1d')
URL = "http://54.159.26.127/api/predictions"
PARAMS = {'companies':' '.join(selections_for_prediction)}

col1_prediction, col2_prediction = st.beta_columns(2)
try:
    if len(selections_for_prediction) > 0:
        r = rq.get(url = URL, params = PARAMS, timeout=(5, 50))
        col1_prediction.write('## Predictions for tomorrow')
        col1_prediction.write(r.json()['0'], orient= 'columns')
        col2_prediction.write('## Stock price today')
        #col2_prediction.write(pd.DataFrame.from_dict(r.json()['1'], orient= 'columns'))
        col2_prediction.write(r.json()['1'], orient= 'columns')
       
            
            
            
except Exception as e :
    print(e)
    st.write('There is not data available for one of the stocks you picked')
#t.write( pd.DataFrame.from_dict(r.json()['0'], orient= 'columns').subtract(pd.DataFrame.from_dict(r.json()['1'], orient= 'columns'), fill_value=0))