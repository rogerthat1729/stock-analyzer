from datetime import date
from jugaad_data.nse import stock_df, NSELive
import plot
import pandas as pd

symbols = pd.read_csv('ind_nifty50list.csv')

def get_stock_data():
    return plot.get_current_data()
