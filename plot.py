import time
import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline as po
import plotly.io as pio
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
    startdate = enddate
    if(duration=="week"):
        startdate -= relativedelta(weeks=1)
    elif(duration=="month"):
        startdate -= relativedelta(months=1)
    elif(duration=="year"):
        startdate -= relativedelta(years=1)
    elif(duration=="fiveyear"):
        startdate -= relativedelta(years=5)
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

def create_plot(data, entity, duration):
    # plt.figure(figsize=(10, 6))
    # plt.style.use('ggplot')
    # for i, sym in enumerate(data):
    #     plt.plot(data[sym]["DATE"], data[sym][entity], color = mpl.colormaps.get_cmap('tab10')(i), label = sym)
    # entity_strings = {'OPEN':'Opening Price', 'CLOSE':'Closing Price', 'LTP': 'Last Traded Price'}
    # duration_strings = {'week':'Last Week', 'month':'Last Month', 'year':'Last Year', 'fiveyear':'Last 5 Years'}
    # plt.title(f'{entity_strings[entity]} vs Date for these stocks for the {duration_strings[duration]}')
    # plt.xlabel('Date')
    # plt.ylabel(entity)
    # plt.grid(visible=False)
    # plt.legend()
    fig = go.Figure()

    for cnt, sym in enumerate(data):
            fig.add_trace(go.Scatter(x=data[sym]["DATE"], y=data[sym][entity],
                                    mode='lines',
                                    name=sym,
                                    line=dict(color=px.colors.qualitative.Set1[cnt])))
    entity_strings = {'OPEN': 'Opening Price', 'CLOSE': 'Closing Price', 'LTP': 'Last Traded Price'}
    duration_strings = {'week': 'Last Week', 'month': 'Last Month', 'year': 'Last Year', 'fiveyear': 'Last 5 Years'}

    fig.update_layout(title=f'{entity_strings[entity]} vs Date for these stocks for the {duration_strings[duration]}',
                    xaxis_title='Date',
                    yaxis_title=entity,
                    showlegend=True,
                    template='plotly_dark')
    return fig

