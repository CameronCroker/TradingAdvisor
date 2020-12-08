
#Description: This function retrieves data from yahoo and writes to a csv (input: list)


#import the libraries
import datetime as dt
import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import os
plt.style.use('fivethirtyeight')

#Get the stock symbols for the portfolio
#We are going to use FAANG

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2020, 1, 1)


def get_my_portfolio(stocks, start=start, end=end):
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    for ticker in stocks:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker, 'yahoo', start, end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except KeyError:
                pass
        else:
            print('Already have {}'.format(ticker))

