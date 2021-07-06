# Stocks_prediction

The objective of this project was to create a web app that allow the users to  know the best stocks of the week and how they are in comparison with the last week, compare stocks based on the user choice and predict prices of the stocks that the user choose, using Long short term memory (LSTM) networks . In particular, the user can analyze a stock from  three different angles its close price, low price and high price. The app was built using Streamlit (simple web app framework for analytics and machine learning apps), Flask, pandas, yfinance, keras, scikit-learn and numpy. The web app is conformed by two files:

1. [streamlit_app.py](https://github.com/jglobaton10/Stocks_prediction/blob/main/streamlit_app.py): This is the web app itself, it is a mix of front end and back end. Here the user can see the best stocks and compare stocks. Also, this script makes requests and show the prices of the predicted stocks.  
2. [LSTM_predictions](https://github.com/jglobaton10/Stocks_prediction/blob/main/1.py): This file is in charge of responding to the requests of the previous one, using a flask API. It trains a LSTM with data from the last 60 days and based and it answers back with the price of the stock for the next day.


The data used in the web app and for trained the models is obtained from the **yfinance** API, which contains historical and real time data of stocks. 

## Enviroment
The scripts can be executed locally: 
1.  Use the command python3 [LSTM_predictions](https://github.com/jglobaton10/Stocks_prediction/blob/main/1.py).py to run the forecasting model
2.  streamlit run  [LSTM_predictions](https://github.com/jglobaton10/Stocks_prediction/blob/main/1.py) to run the web app  

**Requires Python 3.9.5**

Aditionally the web app can accessed in this [Link](). In this case the app will be running on a EC2 instance of **AWS**.

## Dependencies 
- yfinance
- Streamlit
- pandas
- scikit-learn
- numpy
- flask
- flask-restful
- flask-marshmallow 

## Images of the app 
![image](https://github.com/jglobaton10/Stocks_prediction/blob/main/streamlit_app-%C2%B7-Streamlit-Google-Chrome-2021-07-06-19-32-27.gif)
)
![image](https://user-images.githubusercontent.com/47225250/124680040-923d9400-de93-11eb-82ce-9e81f29bac17.png)
)
