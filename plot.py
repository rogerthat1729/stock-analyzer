import time
import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import stock_df
from io import BytesIO
import base64

stock_list = ["ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJFINANCE", 
                "BAJAJFINSV", "BPCL", "BHARTIARTL", "BRITANNIA", "CIPLA", "COALINDIA", 
                "DIVISLAB", "DRREDDY", "EICHERMOT", "GRASIM", "HCLTECH", "HDFCBANK", 
                "HDFCLIFE", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "HDFC", "ICICIBANK", 
                "ITC", "IOC", "INDUSINDBK", "INFY", "JSWSTEEL", "KOTAKBANK", "LT", 
                "M&M", "MARUTI", "NTPC", "NESTLEIND", "ONGC", "POWERGRID", "RELIANCE", 
                "SBILIFE", "SHREECEM", "SBIN", "SUNPHARMA", "TCS", "TATACONSUM", "TATAMOTORS", 
                "TATASTEEL", "TECHM", "TITAN", "UPL", "ULTRACEMCO", "WIPRO"]

def give_dates(duration):
    enddate = datetime.now().date()
    if(duration=="week"):
        startdate = enddate - relativedelta(weeks=1)
    elif(duration=="month"):
        startdate = enddate - relativedelta(months=1)
    elif(duration=="year"):
        startdate = enddate - relativedelta(years=1)
    elif(duration=="fiveyear"):
        startdate = enddate - relativedelta(years=5)
    return (startdate, enddate)

def give_data(symbols, duration):
    # startdate = datetime.strptime(startdate, '%Y-%m-%d').date()
    # enddate = datetime.strptime(enddate, '%Y-%m-%d').date()
    dataframes = {}
    dates = give_dates(duration)
    for sym in symbols:
        df = stock_df(symbol=sym, from_date=dates[0], 
                    to_date=dates[1], series="EQ")
        dataframes[sym] = df
    cols = ["DATE", "OPEN", "CLOSE", "HIGH", "LOW", "LTP", "VOLUME", "VALUE", "NO OF TRADES"]
    data = {}
    for sym in dataframes:
        data[sym] = dataframes[sym][cols]
    return data

def plot_to_url(plt):
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    buffer = b''.join(buf)
    buffer_base64 = base64.b64encode(buffer)
    plt.close()
    return buffer_base64.decode('utf-8')

def create_plot(data, entity, duration):
    plt.figure(figsize=(10, 6))
    plt.style.use('ggplot')
    for i, sym in enumerate(data):
        plt.plot(data[sym]["DATE"], data[sym][entity], color = mpl.colormaps.get_cmap('tab10')(i), label = sym)
    entity_strings = {'OPEN':'Opening Price', 'CLOSE':'Closing Price', 'LTP': 'Last Traded Price'}
    duration_strings = {'week':'Last Week', 'month':'Last Month', 'year':'Last Year', 'fiveyear':'Last 5 Years'}
    plt.title(f'{entity_strings[entity]} vs Date for these stocks for the {duration_strings[duration]}')
    plt.xlabel('Date')
    plt.ylabel(entity)
    plt.grid(visible=False)
    plt.legend()
    return plot_to_url(plt)

