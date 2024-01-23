from datetime import date
from jugaad_data.nse import stock_df
from dateutil.relativedelta import relativedelta
import time
import os
import argparse
import matplotlib.pyplot as plt
import pandas as pd


# def get_stock_data():
#     # Example to fetch stock data, modify as per your requirements
#     stock_list = ["SBIN"]
#     stock_data = []
#     # Today's date
#     today = date(2024, 1, 1)
#     # x years ago date 
#     years_ago = today - relativedelta(years = 5)
#     for stock in stock_list:
#         data = stock_df(symbol=stock, from_date= years_ago,to_date=today, series="EQ")
#         stock_data.append({"name": stock, "data": data})
#     return stock_data
def get_stock_data():
    # List of NIFTY 50 stock symbols
    # stock_list = ["ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", 
    #               "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", 
    #               "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", 
    #               "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "HDFC", "ICICIBANK", 
    #               "ITC", "IOC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", 
    #               "M&M", "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", 
    #               "SBILIFE", "SHREECEM", "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", 
    #               "TATASTEEL", "TECHM", "TITAN", "UPL", "ULTRACEMCO", "WIPRO"]
    
    stock_list = ["SBIN","ADANIPORTS"]

    stock_data = []
    # Today's date (modify accordingly)
    today = date.today()
    # x years ago date 
    years_ago = today - relativedelta(years=5)
    
    for stock in stock_list:
        try:
            data = stock_df(symbol=stock, from_date=years_ago, to_date=today, series="EQ")
            stock_data.append({"name": stock, "data": data})
            time.sleep(1)  # To prevent rapid requests
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")
    
    return stock_data
