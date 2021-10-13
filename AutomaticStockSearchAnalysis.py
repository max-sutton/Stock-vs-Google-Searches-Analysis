# To use dataframes & view csv file from google
import pandas as pd
from pandas import Series, DataFrame
from pandas.tseries.frequencies import to_offset
import numpy as np

# To visualize data
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

from datetime import datetime

# To get data from yahoo
import pandas_datareader as pdr

# To get search data from google
import pytrends
from pytrends.request import TrendReq

# To find linear regression equation and confidence in model
import statsmodels.api as sm

stock = input('Please Enter a stock Ticker: ')

end = datetime.now()
start = datetime(end.year - 5, end.month, end.day)

# Retrieve the data. Each stock historical data stored under dataframe object named under stock ticker
dfstock = pdr.get_data_yahoo(stock, start, end)


def convert_to_weekly(df):
    # Resample all of the data to convert data to weekly
    output = df.resample('W').apply(
        {'Open': 'first',
         'High': 'max',
         'Low': 'min',
         'Close': 'last',
         'Volume': 'sum',
         'Adj Close': 'last'})
    output.index -= to_offset('7D')

    # Output of the new dataframes
    output = output[['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']]
    df = output
    return df


dfstock = convert_to_weekly(dfstock)

pytrend = TrendReq()
pytrend.build_payload(kw_list=[stock],
                      cat=0,
                      timeframe='today 5-y')
sStock = pytrend.interest_over_time()
sStock = sStock.drop(columns='isPartial')

dfstock = pd.concat([dfstock, sStock], axis=1)

dfstock['Return'] = dfstock['Adj Close'].pct_change()
dfstock['Absolute_Pct_Change'] = dfstock['Return'].abs()
dfstock = dfstock.dropna()

modelSStock = sm.OLS(dfstock['Absolute_Pct_Change'], dfstock[stock])
modelSStock = modelSStock.fit()

modelVStock = sm.OLS(dfstock['Volume'], dfstock[stock])
modelVStock = modelVStock.fit()


def Search_Interest_And_Stock_Volume_Res():
    print(stock + ' Search Interest and Stock Volume')
    print(modelVStock.params)
    print('Adj R Squared:', modelVStock.rsquared_adj)
    print('P Value: ', modelVStock.pvalues)
    print()


def Search_Interest_And_Stock_Absolute_Pct_Change_Res():
    print(stock + ' Search Interest and Absolute_Pct_Change')
    print(modelSStock.params)
    print('Adj R Squared:', modelSStock.rsquared_adj)
    print('P Value: ', modelSStock.pvalues)
    print()


Search_Interest_And_Stock_Volume_Res()

Search_Interest_And_Stock_Absolute_Pct_Change_Res()
