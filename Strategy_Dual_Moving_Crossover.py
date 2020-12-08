#short term average crosses the long term average (momentum)
#buy: short crosses above long term
#sell: short crosses below long term

#Description: This program uses the dual moving average crossover to determine when
# to buy and sell stock

#import the libraries
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_datareader import data
plt.style.use('fivethirtyeight')

#store the data
AAPL = pd.read_csv('AAPL.csv')
print(AAPL)

#visualize the data
plt.figure(figsize=(12.5,4.5))
plt.plot(AAPL['Adj Close'], label = 'AAPl')
plt.title('Apple Adj. close price History')
plt.xlabel('january 2010 - December 2016')
plt.ylabel('Adj Close price USD ($)')
plt.legend(loc='upper left')


#Create the simple moving average with a 30 day window
SMA30 = pd.DataFrame()
SMA30['Adj Close Price'] = AAPL['Adj Close'].rolling(window=30).mean()

#Create a simple moving average with a 100 day window
SMA100 = pd.DataFrame()
SMA100['Adj Close Price'] = AAPL['Adj Close'].rolling(window=100).mean()

#Visualize the data
plt.figure(figsize=(12.5, 4.5))
plt.plot(AAPL['Adj Close'], label='AAPl')
plt.plot(SMA30['Adj Close Price'], label='SMA30')
plt.plot(SMA100['Adj Close Price'], label='SMA100')
plt.title('Apple Adj. close price History')
plt.xlabel('january 2010 - December 2016')
plt.ylabel('Adj Close price USD ($)')
plt.legend(loc='upper left')


#Create a new data frame to store all the data
data = pd.DataFrame()
data['AAPL'] = AAPL['Adj Close']
data['SMA30'] = SMA30['Adj Close Price']
data['SMA100'] = SMA100['Adj Close Price']
print(data)

#Create a function to signal when to buy and sell the asset/stock
def buy_sell(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['AAPL'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['AAPL'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy,sigPriceSell)

buy_sell = buy_sell(data)
data['Buy_Signal_Price'] = buy_sell[0]
data['Sell_Signal_Price'] = buy_sell[1]

#Show the data
print(data)


#visualizee the data and the strategy to buy and sell
plt.figure(figsize=(12.6, 4.6))
plt.plot(data['AAPL'], label='AAPl', alpha = 0.35)
plt.plot(data['SMA30'], label='SMA30', alpha = 0.35)
plt.plot(data['SMA100'], label='SMA100', alpha = 0.35)
plt.scatter(data.index, data['Buy_Signal_Price'], label='Buy', marker='^',color = 'green')
plt.scatter(data.index, data['Sell_Signal_Price'], label='Sell', marker='v',color = 'red')
plt.title('Apple Adj. Close Price history Buy and Sell Signal')
plt.xlabel('January 2010 - December 2016')
plt.ylabel('Adj Close price USD ($)')
plt.legend(loc='upper left')


plt.show()