# description: This program uses the moving Average Convergence/Divergence (MACD crossover
# to determine when to buy and sell stock.

# description: this program attempts to optimize a users portfolio using Efficient Frontier

#import the libraries
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_datareader import data as web
plt.style.use('fivethirtyeight')

#store the data
AAPL = pd.read_csv('TSLA.csv')

#Set the date as the index
AAPL = AAPL.set_index(pd.DatetimeIndex(AAPL['Date'].values))

#Calculate the simple moving average, standard deviation, upper band and the lower band
#Get the time period (20 day)
period = 20

#Calculate the simple mpvomg average
AAPL['SMA'] = AAPL['Adj Close'].rolling(window=period).mean()

#Get the standard deviation
AAPL['STD'] = AAPL['Adj Close'].rolling(window=period).std()

#Calculate the upper bollinger band
AAPL['Upper_Narrow'] = AAPL['SMA'] + (AAPL['STD'] * 1.1)

AAPL['Upper'] = AAPL['SMA'] + (AAPL['STD'] * 2)

#Calculate the lower bollinger band
AAPL['Lower_Narrow'] = AAPL['SMA'] - (AAPL['STD'] * 1)

#Calculate the lower bollinger band
AAPL['Lower'] = AAPL['SMA'] - (AAPL['STD'] * 2)

#Calculate the MACD and signal line indicators
#Calculate the short term exponential moving average (EMA)
ShortEMA = AAPL.Close.ewm(span=12, adjust=False).mean()
#Calculate the long term exponential moving average
LongEMA = AAPL.Close.ewm(span=26, adjust=False).mean()

#Calculate the MACD line
MACD = ShortEMA - LongEMA

#Span 9 period exponentially smooth average of the macd line
signal = MACD.ewm(span=9, adjust=False).mean()

#Create new columns for the data
AAPL['MACD'] = MACD
AAPL['Signal Line'] = signal

#Dual moving Average
#Create the simple moving average with a 30 day window
SMA30 = pd.DataFrame()
SMA30['Adj Close Price'] = AAPL['Adj Close'].rolling(window=30).mean()

#Create a simple moving average with a 100 day window
SMA100 = pd.DataFrame()
SMA100['Adj Close Price'] = AAPL['Adj Close'].rolling(window=100).mean()

#Create a new data frame to store all the data
AAPL['SMA30'] = SMA30['Adj Close Price']
AAPL['SMA100'] = SMA100['Adj Close Price']

# Calculate the three moving averages
# Calculate the short/fast exponential moving average
ShortEMA = AAPL.Close.ewm(span=5, adjust=False).mean()

# Calculate the long/slow exponential moving average
LongEMA = AAPL.Close.ewm(span=63, adjust=False).mean()

# Calculate the middle/medium exponential moving average
MiddleEMA = AAPL.Close.ewm(span=21, adjust=False).mean()


# Add the exponential moving averages to the data set
AAPL['Short'] = ShortEMA
AAPL['Middle'] = MiddleEMA
AAPL['Long'] = LongEMA


#prepare the data to calculate the RSI
#Get the Difference in price from the previous day
delta = AAPL['Adj Close'].diff(1)

#Get rid of NaN
delta = delta.dropna()

#Get the positive gains (up) and the negative gains (down)
up = delta.copy()
down = delta.copy()

up[up<0] = 0
down[down>0] = 0

#Get the time period, (usually 14 days)
period = 14

#Calculate the average gain and the average loss
AVG_Gain = up.rolling(window=period).mean()
AVG_Loss = abs(down.rolling(window=period).mean())

#Calculate the RSI
#Calculate the Relative Strength (RS)
RS = AVG_Gain/AVG_Loss

#Calculatet the Relative Strength Index (RSI)
RSI = 100 - (100.0/(1.0 + RS))

#Create a new data frame
new_df = pd.DataFrame()
new_df['Adj Close'] = AAPL['Adj Close']
new_df['RSI'] = RSI


#Create a function to signal when to buy an asset
def buy_sell(signal):
    Buy = []
    Sell = []
    flag = -1
    for i in range(0, len(signal)):
        if i == len(signal)-1:
            Buy.append(np.nan)
            Sell.append(np.nan)
        elif signal['MACD'][i] > signal['MACD'][i+1]:
            Sell.append(np.nan)
            if flag != 1:
                Buy.append(signal['Close'][i])
                flag = 1
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['MACD'][i+1]:
            Buy.append(np.nan)
            if flag != 0:
                Sell.append(signal['Close'][i])
                flag = 0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)

    return Buy, Sell



#Create Buy and Sell Column
a = buy_sell(AAPL)
AAPL['Momentum_up'] = a[0]
AAPL['Momentum_down'] = a[1]




#Create a function to signal when to buy and sell the asset/stock
def buy_sell_dmac(data):
    sigPriceBuy = []
    sigPriceSell = []
    flag = -1

    for i in range(len(data)):
        if data['SMA30'][i] > data['SMA100'][i]:
            if flag != 1:
                sigPriceBuy.append(data['Close'][i])
                sigPriceSell.append(np.nan)
                flag = 1
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        elif data['SMA30'][i] < data['SMA100'][i]:
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(data['Close'][i])
                flag = 0
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)

    return (sigPriceBuy,sigPriceSell)

buy_sell = buy_sell_dmac(AAPL)
AAPL['Moving_Average_Buy'] = buy_sell[0]
AAPL['Moving_Average_Sell'] = buy_sell[1]

#Create a function to signal when to buy an asset
def buy_sell_macd(signal):
    Buy = []
    Sell = []
    flag = -1

    for i in range(0, len(signal)):
        if signal['MACD'][i] > signal['Signal Line'][i]:
            Sell.append(np.nan)
            if flag != 1:
                Buy.append(signal['Close'][i])
                flag = 1
            else:
                Buy.append(np.nan)
        elif signal['MACD'][i] < signal['Signal Line'][i]:
            Buy.append(np.nan)
            if flag != 0:
                Sell.append(signal['Close'][i])
                flag = 0
            else:
                Sell.append(np.nan)
        else:
            Buy.append(np.nan)
            Sell.append(np.nan)

    return Buy, Sell

#Create Buy and Sell Column
a = buy_sell_macd(AAPL)
AAPL['Momentum_Buy'] = a[0]
AAPL['Momentum_Sell'] = a[1]


#Create a new data frame
bollinger_df = pd.DataFrame()
bollinger_df = AAPL[period-1:]
print(new_df)

#Creat a function to get the buy and sell signals
def get_signal(data):
    buy_signal = []
    sell_signal = []

    for i in range(len(data['Close'])):
        if data['Close'][i] > data['Upper'][i]: #then you should sell
            buy_signal.append(np.nan)
            sell_signal.append(data['Close'][i])
        elif data['Close'][i] < data ['Lower'][i]:
            buy_signal.append(data['Close'][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)
    return(buy_signal,sell_signal)


#Create two new columns
a = get_signal(bollinger_df)
bollinger_df.loc[:,'Buy'] = a[0]
bollinger_df.loc[:,'Sell'] = a[1]

#Remove NaN
buy = pd.DataFrame()
buy = bollinger_df.loc[:,'Buy']
sell = pd.DataFrame()
sell = bollinger_df.loc[:,'Sell']

buy.dropna(inplace=True)
sell.dropna(inplace=True)





# Create the function to buy and sell the stock
def buy_sell_function(data):
    buy_list = []
    sell_list = []
    flag_long = False
    flag_short = False

    for i in range(0, len(data)):
        if data['Long'][i] > data['Middle'][i] and data['Middle'][i] > data['Short'][i] and flag_long == False and flag_short == False:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_short = True
        elif flag_short == True and data['Short'][i] > data['Middle'][i]:
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_short = False
        elif data['Long'][i] < data['Middle'][i]  and data['Middle'][i] < data['Short'][i] and flag_long == False and flag_short == False and data['Close'][i] < data['Lower'][i]:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
        elif flag_long == True and data['Short'][i] < data['Middle'][i]:
            sell_list.append(data['Close'][i])
            buy_list.append(np.nan)
            flag_long = False
        else:
            buy_list.append(np.nan)
            sell_list.append(np.nan)

    return(buy_list,sell_list)


#add the buy and sell signals to the data set
a = buy_sell_function(AAPL)
AAPL['Buy'] = a[0]
AAPL['Sell'] = a[1]



# Create the function to buy and sell the stock
def strategy_function(data):
    buy_list = []
    sell_list = []
    flag_buy = False
    flag_sell = False
    flag_long = False
    flag_short = False

    for i in range(0, len(data)):
        if data['Long'][i] > data['Middle'][i] and data['Middle'][i] > data['Short'][i] and flag_long == False and flag_short == False and data['Close'][i] < data['Lower_Narrow'][i] and flag_buy != True:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_short = True
            flag_buy = True
            flag_sell = False
        elif flag_short == True and data['Short'][i] > data['Middle'][i] and data['Close'][i] > data['Upper_Narrow'][i]:
            sell_list.append(np.nan)
            buy_list.append(np.nan)
            flag_short = False
        elif data['Long'][i] < data['Middle'][i]  and data['Middle'][i] < data['Short'][i] and flag_long == False and flag_short == False and data['Close'][i] < data['Lower_Narrow'][i] and flag_buy != True:
            buy_list.append(data['Close'][i])
            sell_list.append(np.nan)
            flag_long = True
            flag_buy = True
            flag_sell = False
        elif flag_long == True and data['Short'][i] < data['Middle'][i] and data['Close'][i] > data['Upper_Narrow'][i]:
            sell_list.append(np.nan)
            buy_list.append(np.nan)
            flag_long = False
        elif data['MACD'][i] < data['Signal Line'][i] and data['Close'][i] > data['Upper_Narrow'][i]:
            buy_list.append(np.nan)
            if flag_sell != True:
                sell_list.append(data['Close'][i])
                flag_sell = True
                flag_buy = False
            else:
                sell_list.append(np.nan)
        elif data['Close'][i] > data['Upper'][i] and flag_sell != True:  # then you should sell
            buy_list.append(np.nan)
            sell_list.append(data['Close'][i])
            flag_sell = True
            flag_buy = False
        else:
            sell_list.append(np.nan)
            buy_list.append(np.nan)

    return(buy_list,sell_list)

a = strategy_function(AAPL)
AAPL['Strat_Buy'] = a[0]
AAPL['Strat_Sell'] = a[1]

#Visually show the stock buy and sell signals
#Create a list of columns to keep
column_list = ['Close', 'SMA','Short','Middle','Long','Upper','Lower']

#plot the data
AAPL[column_list].plot(alpha=0.35, figsize=(12.2, 6.4))
plt.scatter(AAPL.index, AAPL['Momentum_up'], color='blue', label='Momentum_up',lw = 3, marker='>', alpha=1)
plt.scatter(AAPL.index, AAPL['Momentum_down'], color='y', label='Momentum_down',lw = 3, marker='<', alpha=1)
plt.scatter(AAPL.index, AAPL['Moving_Average_Buy'], color='m', label='Moving_Average_Buy',lw = 3, marker='p', alpha=1)
plt.scatter(AAPL.index, AAPL['Moving_Average_Sell'], color='k', label='Moving_Average_Sell',lw = 3, marker='s', alpha=1)
plt.scatter(AAPL.index, AAPL['Momentum_Buy'], label='Momentum_Buy', marker='^',lw = 3,color='green')
plt.scatter(AAPL.index, AAPL['Momentum_Sell'], label='Momentum_Sell', marker='v',lw = 3,color='red')
plt.scatter(AAPL.index, AAPL['Buy'], color = 'green', label = 'Three Moving Buy', marker = '^',lw =3)
plt.scatter(AAPL.index, AAPL['Sell'], color = 'red', label = 'Three Moving Sell', marker = 'v',lw =3)
plt.scatter(buy.index, buy, color = 'gold',lw = 3,label = 'Bollinger_buy', marker = '>')
plt.scatter(sell.index, sell, color = 'Red',lw = 3,label = 'Bollinger_sell', marker = '<')
plt.fill_between(AAPL.index, AAPL['Upper'],AAPL['Lower'], color = 'grey', alpha = 0.35)
plt.scatter(AAPL.index, AAPL['Strat_Buy'], color = 'gold', label = 'Strategy_buy', marker = '>',lw =3)
plt.scatter(AAPL.index, AAPL['Strat_Sell'], color = 'black', label = 'Strategy_Sell', marker = '<',lw =3)

plt.plot(new_df.index,new_df['RSI'])
plt.axhline(0,linestyle = '--', alpha = 0.5, color= 'grey')
plt.axhline(10,linestyle = '--', alpha = 0.5, color= 'orange')
plt.axhline(20,linestyle = '--', alpha = 0.5, color= 'green')
plt.axhline(30,linestyle = '--', alpha = 0.5, color= 'red')
plt.axhline(70,linestyle = '--', alpha = 0.5, color= 'red')
plt.axhline(80,linestyle = '--', alpha = 0.5, color= 'green')
plt.axhline(90,linestyle = '--', alpha = 0.5, color= 'orange')
plt.axhline(100,linestyle = '--', alpha = 0.5, color= 'grey')
plt.legend(loc='upper left')
plt.title('Bollinger Band for Apple')
plt.ylabel('USD Price ($)')

#plot the data
# column_list = ['Close', 'SMA', 'Upper', 'Lower']
# AAPL[column_list].plot(alpha=0.50, figsize=(12.2, 6.4))
# plt.legend(loc='upper left')
# plt.title('Bollinger Band for Apple')
# plt.ylabel('USD Price ($)')

#Visually show the stock buy and sell signals

#visualizee the data and the strategy to buy and sell

#Visually show the stock buy and sell signals


# #Create a list of columns to keep
# column_list = ['Close', 'SMA', 'Upper', 'Lower']

# #plot the data
# AAPL[column_list].plot(alpha=0.50, figsize=(12.2, 6.4))
# plt.scatter(AAPL.index, AAPL['Momentum_up'], color='blue', label='Momentum_up',lw = 3, marker='>', alpha=1)
# plt.scatter(AAPL.index, AAPL['Momentum_down'], color='y', label='Momentum_down',lw = 3, marker='<', alpha=1)
# plt.scatter(AAPL.index, AAPL['Moving_Average_Buy'], color='m', label='Moving_Average_Buy',lw = 3, marker='p', alpha=1)
# plt.scatter(AAPL.index, AAPL['Moving_Average_Sell'], color='k', label='Moving_Average_Sell',lw = 3, marker='s', alpha=1)
# plt.scatter(AAPL.index, AAPL['Momentum_Buy'], label='Momentum_Buy', marker='^',lw = 3,color='green')
# plt.scatter(AAPL.index, AAPL['Momentum_Sell'], label='Momentum_Sell', marker='v',lw = 3,color='red')
#
#
#
# plt.legend(loc='upper left')
# plt.title('Bollinger Band for Apple')
# plt.ylabel('USD Price ($)')







# ## Fix the Below ###
# print(new_df)
# #plot and shade the area between the two bollinger bands
# #Get the figure and the figure size
# fig = plt.figure(figsize=(12.2, 6.4))
# #Add the subplot
# ax =fig.add_subplot(111)
# #Get the index value of the data frame
# x_axis = new_df.index
# #plot and shade the area between the upper and lower band
#
#
# #Plot the closing price and the SMA
# # ax.plot(x_axis, new_df['Close'],color = 'gold', lw = 3, label = 'Close Price')
# # ax.plot(x_axis, new_df['SMA'],color = 'blue', lw = 3, label = 'SMA')
# # ax.set_title('Bollinger band for Apple')
# # ax.set_xlabel('Date')
# # ax.set_ylabel('USD Price ($)')
# # plt.xticks(rotation = 45)
# # ax.legend

plt.show()