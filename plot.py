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
    mn_price = 1e9
    mx_price = 0

    for cnt, sym in enumerate(data):
            fig.add_trace(go.Scatter(x=data[sym]["DATE"], y=data[sym][entity],
                                    mode='lines',
                                    name=sym,
                                    line=dict(color=px.colors.qualitative.Set1[cnt])))
            mn_price = min(mn_price, min(data[sym][entity]))
            mx_price = max(mx_price, max(data[sym][entity]))
            
    entity_strings = {'OPEN': 'Opening Price', 'CLOSE': 'Closing Price', 'LTP': 'Last Traded Price'}
    # duration_strings = {'week': 'Last Week', 'month': 'Last Month', 'year': 'Last Year', 'fiveyear': 'Last 5 Years'}

    fig.update_layout(title=f'{entity_strings[entity]} vs Date for these stocks',
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
                        range = [mn_price, mx_price],
                        showgrid=True,
                        zeroline=False,
                        showline=False,
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

