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

def plot(symbol, startdate, enddate):
    startdate = datetime.strptime(startdate, '%Y-%m-%d').date()
    enddate = datetime.strptime(enddate, '%Y-%m-%d').date()
    df = stock_df(symbol=symbol, from_date=startdate, 
                to_date=enddate, series="EQ")
    cols = ["DATE", "OPEN", "CLOSE", "HIGH", "LOW", "LTP", "VOLUME", "VALUE", "NO OF TRADES"]
    data = df[cols]
    plt.style.use('ggplot')
    plt.plot(data["DATE"], data["OPEN"])
    plt.xlabel('Date')
    plt.ylabel('Opening Price')
    plt.grid(visible=False)
    plt.show()

