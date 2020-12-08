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
AAPL = pd.read_csv('GOOG.csv')

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


#Calculaate the typical price
typical_price = (AAPL['Close'] + AAPL['High'] + AAPL['Low'] )/3
typical_price

#Get the period typically MFI uses a preiod of 14 days
period = 14

#Calculate the money flow
money_flow = typical_price * AAPL['Volume']

# Get all of the positive and negative money flows
positive_flow = []
negative_flow = []

#Loop through the typical price
for i in range(1,len(typical_price)):
    if typical_price[i] > typical_price[i-1]:
        positive_flow.append(money_flow[i-1])
        negative_flow.append(0)
    elif typical_price[i] < typical_price[i-1]:
        negative_flow.append(money_flow[i-1])
        positive_flow.append(0)
    else:
        negative_flow.append(0)
        positive_flow.append(0)

#Get all of the positive and negative money flows within the time period
positive_mf = []
negative_mf = []

for i in range(period-1,len(positive_flow)):
    positive_mf.append(sum(positive_flow[i+1 - period : i+1]))      #should be 14 values
for i in range(period-1,len(negative_flow)):
    negative_mf.append(sum(negative_flow[i+1 - period : i+1]))      #should be 14 values

#Calculate the money flow index
mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))
mfi


backtest = 3400

# Create the function to buy and sell the stock
def strategy_function(data,mfi = 50):
    buy_list = []
    sell_list = []
    free_cash = 20000
    last_buy = 0
    profit = 0
    returns = pd.DataFrame()
    flag_buy = False
    flag_long = False
    flag_short = False

    for i in range(0, len(data)):
        if data['Long'][i] > data['Middle'][i] > data['Short'][i] and flag_long == False and flag_short == False and data['MACD'][i] > data['Signal Line'][i] and data['MFI'][i] < mfi and flag_buy != True:
            buy_list.append(data['Close'][i])
            free_cash = free_cash - data['Close'][i]
            last_buy = data['Close'][i]
            sell_list.append(np.nan)
            flag_short = True
            flag_buy = True
        elif flag_short == True and data['Short'][i] > data['Middle'][i] and data['MACD'][i] < data['Signal Line'][i] and data['MFI'][i] > mfi and flag_buy == True:
            sell_list.append(data['Close'][i])
            free_cash = free_cash + data['Close'][i]
            profit = profit + (data['Close'][i] - last_buy)
            buy_list.append(np.nan)
            flag_short = False
            flag_buy = False
        elif data['Long'][i] < data['Middle'][i] < data['Short'][i] and flag_long == False and flag_short == False and data['MACD'][i] > data['Signal Line'][i] and data['MFI'][i] < mfi and flag_buy != True:
            buy_list.append(data['Close'][i])
            free_cash = free_cash - data['Close'][i]
            last_buy = data['Close'][i]
            sell_list.append(np.nan)
            flag_long = True
            flag_buy = True
        elif flag_long == True and data['Short'][i] < data['Middle'][i] and data['MACD'][i] < data['Signal Line'][i] and data['MFI'][i] > mfi and flag_buy == True:
            sell_list.append(data['Close'][i])
            free_cash = free_cash + data['Close'][i]
            profit = profit + (data['Close'][i] - last_buy)
            buy_list.append(np.nan)
            flag_buy = False
            flag_long = False
        else:
            sell_list.append(np.nan)
            buy_list.append(np.nan)

    print('profit: ' + str(profit))

    return(buy_list,sell_list)


df3 = AAPL[period:]
df3['MFI'] = mfi
df3 = df3[backtest:]
a = strategy_function(df3)
df3['Strat_Buy'] = a[0]
df3['Strat_Sell'] = a[1]
Strat_Buy = df3['Strat_Buy']
Strat_sell = df3['Strat_Sell']

Strat_Buy.dropna(inplace=True)
Strat_sell.dropna(inplace=True)
#Visually show the stock buy and sell signals
#Create a list of columns to keep
column_list = ['Close', 'SMA','Short','Middle','Long','Upper','Lower']

#plot the data
AAPL[column_list].plot(alpha=0.35, figsize=(12.2, 6.4))
plt.fill_between(AAPL.index, AAPL['Upper'],AAPL['Lower'], color = 'grey', alpha = 0.35)
plt.scatter(Strat_Buy.index,Strat_Buy, color = 'green', label = 'Strategy_buy', marker = '^',lw =3)
plt.scatter(Strat_sell.index, Strat_sell, color = 'red', label = 'Strategy_Sell', marker = 'v',lw =3)

plt.legend(loc='upper left')
plt.title('Bollinger Band for Apple')
plt.ylabel('USD Price ($)')

plt.show()

