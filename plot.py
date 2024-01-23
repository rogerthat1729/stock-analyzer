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

def return_dataframe(symbol, startdate, enddate):
     df = stock_df(symbol=symbol, from_date=startdate, 
                    to_date=enddate, series="EQ")
     return df
