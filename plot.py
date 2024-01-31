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
from jugaad_data.nse import stock_df, index_df
from nsetools import Nse

entity_strings = {'OPEN': 'Opening Price', 'CLOSE': 'Closing Price', 'LOW': 'Intraday Low', 'HIGH':'Intraday High', 'LTP':'Last Traded Price', 'VOLUME':'Volume', 'VALUE':'Value', 'NO OF TRADES':'No of Trades'}
type_strings = {'normal': 'Line Plot', 'candle': 'Candlestick Plot'}

def give_dates(duration):
    enddate = datetime.now().date()
    enddate -= timedelta(days=enddate.weekday())
    startdate = enddate
    if(duration=="week"):
        startdate -= relativedelta(weeks=1)
    elif(duration=='day'):
        startdate -= relativedelta(days=1)
    elif(duration=="month"):
        startdate -= relativedelta(months=1)
    elif(duration=="year"):
        startdate -= relativedelta(years=1)
    elif(duration=="fiveyear"):
        startdate -= relativedelta(years=5)
    return (startdate, enddate)

def give_data(symbols):
    dataframes = {}
    dates = give_dates('fiveyear')
    for sym in symbols:
        df = stock_df(symbol=sym, from_date=dates[0], 
                    to_date=dates[1], series="EQ")
        dataframes[sym] = df
    cols = ["DATE", "OPEN", "CLOSE", "HIGH", "LOW", "LTP", "VOLUME", "VALUE", "NO OF TRADES"]
    data = {}
    for sym in dataframes:
        data[sym] = dataframes[sym][cols]
    return data

def create_plot(data, entity, type, plottype):
    fig = go.Figure()
    date = 'DATE'
    if type == 'index':
        date = 'HistoricalDate'
    for cnt, sym in enumerate(data):
        if plottype == 'normal':
            fig.add_trace(go.Scatter(x=data[sym][date], y=data[sym][entity],
                                    mode='lines',
                                    name=sym))
        else:
            fig.add_trace(go.Candlestick(x=data[sym][date],
                                        open=data[sym]['OPEN'],
                                        high=data[sym]['HIGH'],
                                        low=data[sym]['LOW'],
                                        close=data[sym]['CLOSE'],
                                        name=sym,
                                        increasing_line_color= 'green', decreasing_line_color= 'red'))

    fig.update_layout(title=f'{type_strings[plottype]} {entity_strings[entity]} vs Date for these stocks',
                    xaxis_title='Date',
                    yaxis_title=entity,
                    xaxis = dict(
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=2,
                        ticks='outside',
                        tickfont=dict(
                            family='Arial',
                            size=12,
                            color='rgb(82, 82, 82)',
                        )
                    ),
                    yaxis=dict(
                        showline = True,
                        showgrid=True,
                        zeroline=False,
                        showticklabels=True,
                    ),
                    showlegend=True,
                    plot_bgcolor='white')
    
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeselector_font = dict(size = 10),
        rangeselector_bgcolor = 'rgb(200, 200, 200)',
        rangeselector_font_color = 'rgb(50, 50, 50)'
    )
    return fig

def get_index_data():
    dates = give_dates('fiveyear')
    df = index_df(symbol='NIFTY 50', from_date=dates[0], 
                to_date=dates[1])
    return df

def get_current_data():
    syms = pd.read_csv('ind_nifty50list.csv')
    stock_list = syms['Symbol'].tolist()
    dates = give_dates('day')
    to_sort = []
    for sym in stock_list:
        df = stock_df(symbol=sym, from_date=dates[0], 
                    to_date=dates[1], series="EQ")
        diff = df['CLOSE'].iloc[-1] - df['OPEN'].iloc[-1]
        to_sort.append((diff, sym))
    to_sort.sort()
    all_data = []
    for i in range(len(to_sort)):
        df = stock_df(symbol=to_sort[i][1], from_date=dates[0], 
                    to_date=dates[1], series="EQ")
        data = {}
        data['symbol'] = to_sort[i][1]
        data['open'] = df['OPEN'].iloc[0]
        data['low'] = df['LOW'].iloc[0]
        data['high'] = df['HIGH'].iloc[0]
        data['close'] = df['CLOSE'].iloc[0]
        all_data.append(data)
    return all_data

def get_performers():
    data = get_current_data()
    return (reversed(data[-5:]), data[:5])
