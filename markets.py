from datetime import date
from jugaad_data.nse import stock_df, NSELive
from dateutil.relativedelta import relativedelta
import time
import os
import argparse
import matplotlib.pyplot as plt
import pandas as pd

symbols = pd.read_csv('ind_nifty50list.csv')

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
    # stock_list = ["ADANIPORTS", "ASIANPAINT"]
    stock_list = symbols['Symbol'].tolist()
    parameters = []

    for stock in stock_list:
        now = NSELive()
        quote = now.stock_quote(stock)
        param = {}
        param['Name'] = quote['info']['symbol']
        # param['Industry'] = (quote['info']['industry'])
        param['LastPrice'] = quote['priceInfo']['lastPrice']
        param['IntraDayHigh'] = quote['priceInfo']['intraDayHighLow']['max']
        param['IntraDayLow'] = quote['priceInfo']['intraDayHighLow']['max']
        parameters.append(param)
    return parameters


