# Description:This program uses the three moving average crossover strategy to determine when to buy and sell stock

# import the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

# Load the Data
# store the data
NFLX = pd.read_csv('NFLX.csv')

# Set the date as the index
NFLX = NFLX.set_index(pd.DatetimeIndex(NFLX['Date'].values))

# Give the index a name
NFLX.index.name = 'Date'

# visualize the data (implement a date range function)
plt.figure(figsize=(12.2, 4.5))
plt.plot(NFLX.index, NFLX['Adj Close'], label='Adj Close')
plt.title('Adj. Close Price History')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Adj Close price USD ($)', fontsize=18)

# Calculate the three moving averages
# Calculate the short/fast exponential moving average
ShortEMA = NFLX.Close.ewm(span=5, adjust=False).mean()

# Calculate the long/slow exponential moving average
LongEMA = NFLX.Close.ewm(span=63, adjust=False).mean()

# Calculate the middle/medium exponential moving average
MiddleEMA = NFLX.Close.ewm(span=21, adjust=False).mean()

# Visualize the closing price and the exponential moving averages
plt.figure(figsize=(12.2, 4.5))
plt.plot(NFLX.index, NFLX['Adj Close'], label='Adj Close', color='blue')
plt.plot(ShortEMA, label='Short/Fast EMA', color='red')
plt.plot(MiddleEMA, label='Middle/Medium EMA', color='orange')
plt.plot(LongEMA, label='Long/Slow EMA', color='green')
plt.title('Adj. Close Price History')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Adj Close price USD ($)', fontsize=18)

# Add the exponential moving averages to the data set
NFLX['Short'] = ShortEMA
NFLX['Middle'] = MiddleEMA
NFLX['Long'] = LongEMA


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
        elif data['Long'][i] < data['Middle'][i]  and data['Middle'][i] < data['Short'][i] and flag_long == False and flag_short == False:
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
a = buy_sell_function(NFLX)
NFLX['Buy'] = a[0]
NFLX['Sell'] = a[1]

#Visually show the stock buy and sell signals
plt.figure(figsize=(12.2, 4.5))
plt.plot(NFLX.index, NFLX['Adj Close'], label='Adj Close', color='blue', alpha = 0.35)
plt.plot(ShortEMA, label='Short/Fast EMA', color='red', alpha = 0.35)
plt.plot(MiddleEMA, label='Middle/Medium EMA', color='orange', alpha = 0.35)
plt.plot(LongEMA, label='Long/Slow EMA', color='green', alpha = 0.35)
plt.scatter(NFLX.index, NFLX['Buy'], color = 'green', label = 'Buy', marker = '^',lw =3)
plt.scatter(NFLX.index, NFLX['Sell'], color = 'red', label = 'Sell', marker = 'v',lw =3)
plt.title('Buy and Sell Chart')
plt.xlabel('Date', fontsize=18)
plt.ylabel('Adj Close price USD ($)', fontsize=18)


plt.show()
