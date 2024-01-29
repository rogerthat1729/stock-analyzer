from datetime import date
from jugaad_data.nse import stock_df, NSELive
import pandas as pd

symbols = pd.read_csv('ind_nifty50list.csv')

def get_stock_data():
    stock_list = symbols['Symbol'].tolist()
    parameters = []

    for stock in stock_list:
        now = NSELive()
        quote = now.stock_quote(stock)
        param = {}
        param['Name'] = quote['info']['symbol']
        param['LastPrice'] = quote['priceInfo']['lastPrice']
        param['IntraDayHigh'] = quote['priceInfo']['intraDayHighLow']['max']
        param['IntraDayLow'] = quote['priceInfo']['intraDayHighLow']['max']
        parameters.append(param)
    return parameters
