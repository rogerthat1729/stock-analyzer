import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import stock_df, index_df

entity_strings = {'OPEN': 'Opening Price', 'CLOSE': 'Closing Price', 'LOW': 'Intraday Low', 'HIGH':'Intraday High', 'LTP':'Last Traded Price', 'VOLUME':'Volume', 'VALUE':'Market Cap', 'NO OF TRADES':'No of Trades'}
type_strings = {'normal': 'Line Plot', 'candle': 'Candlestick Plot'}

csv_data = pd.read_csv('merged_stock_industry_marketcap_data.csv')
csv_data = csv_data[['Symbol', 'Industry', 'MarketCap']]
csv_data = csv_data.set_index('Symbol')

syms = pd.read_csv('NIFTY_TOTAL_MARKET.csv')

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

def include_csv_data(data):
    global csv_data
    for df in data:
        ind = csv_data.loc[df['symbol']]['Industry']
        markcap = csv_data.loc[df['symbol']]['MarketCap']
        markcap = "{:,.2f}".format(markcap)
        df['Industry'] = ind if ind else 'Not Available'
        df['MarketCap'] = markcap if markcap else 'Not Available'
    return data

def give_data(symbols):
    global csv_data
    dataframes = {}
    dates = give_dates('fiveyear')
    for sym in symbols:
        df = stock_df(symbol=sym, from_date=dates[0], 
                    to_date=dates[1], series="EQ")
        dataframes[sym] = df
        
        diff = (df['LTP'].iloc[0] - df['OPEN'].iloc[0])/(df['OPEN'].iloc[0])*100
        if diff >= 0:
            dataframes[sym]['sign'] = 1
        else:
            dataframes[sym]['sign'] = 0
        dataframes[sym]['diff'] = "{:.2f}".format(diff)
        
        ind = csv_data.loc[sym]['Industry']
        markcap = csv_data.loc[sym]['MarketCap']
        
        markcap = "{:,.2f}".format(markcap)
        dataframes[sym]['Industry'] = ind if ind else 'Not Available'
        dataframes[sym]['MarketCap'] = markcap if markcap else 'Not Available'
        
    return dataframes

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

    fig.update_layout(title=f'{type_strings[plottype]} of {entity_strings[entity]} vs Date for these stocks',
                    xaxis_title='Date',
                    yaxis_title=entity,
                    xaxis = dict(
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='rgb(204, 204, 204)',
                        linewidth=2,
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
        rangeslider_visible=False,
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
    fig.update_yaxes(showgrid=True,
                      gridwidth=1, 
                      gridcolor='rgb(200, 200, 200)')
    return fig

def get_index_data():
    dates = give_dates('fiveyear')
    df = index_df(symbol='NIFTY 50', from_date=dates[0], to_date=dates[1])
    return df

def get_current_data():
    global syms
    stock_list = syms['Symbol'].tolist()
    dates = give_dates('day')
    to_sort = []
    for sym in stock_list:
        try:
            df = stock_df(symbol=sym, from_date=dates[0], to_date=dates[1], series="EQ")
            if not df.empty:
                diff = (df['LTP'].iloc[0] - df['OPEN'].iloc[0])/(df['OPEN'].iloc[0])*100
                to_sort.append((diff, sym))
        except Exception as e:
            print(f"Data not available for symbol: {sym}. Skipping.")
            continue
    to_sort.sort()
    all_data = []
    for i in range(len(to_sort)):
        df = stock_df(symbol=to_sort[i][1], from_date=dates[0], 
                    to_date=dates[1], series="EQ")
        data = {}
        data = df.iloc[0].to_dict()
        data['symbol'] = to_sort[i][1]
        data['VALUE'] = "{:,}".format(data['VALUE'])
        diff = (df['LTP'].iloc[0] - df['OPEN'].iloc[0])/(df['OPEN'].iloc[0])*100
        if diff >= 0:
            data['sign'] = 1
        else:
            data['sign'] = 0
        data['diff'] = "{:.2f}".format(diff)
        all_data.append(data)
    all_data = include_csv_data(all_data)
    return all_data

def convert_to_dict(df):
    data = {}
    for i in range(len(df)):
        data[df[i]['symbol']] = df[i]
    return data

def get_performers(data):
    return (data[:5], list(reversed(data[-5:])))