import time
import os
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from jugaad_data.nse import stock_df
from io import BytesIO
import base64

def give_data(symbols, startdate, enddate):
    startdate = datetime.strptime(startdate, '%Y-%m-%d').date()
    enddate = datetime.strptime(enddate, '%Y-%m-%d').date()
    dataframes = {}
    for sym in symbols:
        df = stock_df(symbol=sym, from_date=startdate, 
                    to_date=enddate, series="EQ")
        dataframes[sym] = df
    cols = ["DATE", "OPEN", "CLOSE", "HIGH", "LOW", "LTP", "VOLUME", "VALUE", "NO OF TRADES"]
    data = {}
    for sym in dataframes:
        data[sym] = dataframes[sym][cols]
    return data

