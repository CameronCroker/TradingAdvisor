#Description: this program uses the Bollinger band strategy to determine when to buy and sell stock

#import the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
AAPL['Upper'] = AAPL['SMA'] + (AAPL['STD'] * 3)

#Calculate the lower bollinger band
AAPL['Lower'] = AAPL['SMA'] - (AAPL['STD'] * 3)

#Create a list of columns to keep
column_list = ['Close', 'SMA', 'Upper', 'Lower']

#plot the data
AAPL[column_list].plot(alpha=0.50, figsize=(12.2, 6.4))
plt.legend(loc='upper left')
plt.title('Bollinger Band for Apple')
plt.ylabel('USD Price ($)')

#plot and shade the area between the two Bollinger bands
#Get the figure
fig = plt.figure(figsize=(12.2, 6.4))
#Add the subpolot
ax = fig.add_subplot(1,1,1)
#get the index values of the data frame
x_axis = AAPL.index
#Plot and shade the area between the upper band and the lower band
ax.fill_between(x_axis,AAPL['Upper'],AAPL['Lower'],color = 'grey')
#Plot the closing price and the moving average
ax.plot(x_axis,AAPL['Close'], color = 'gold', lw = 3, label = 'Close Price')
ax.plot(x_axis,AAPL['SMA'], color = 'blue', lw = 3, label = 'Simple Moving Average')

#set the title and show the image
ax.set_title('Bollinger Band for Apple')
ax.set_xlabel('Date')
ax.set_ylabel('USD Price ($)')
plt.xticks(rotation=45)
ax.legend()

#Cre3ate a new data frame
new_df = AAPL[period-1:]
new_df = new_df.set_index(pd.DatetimeIndex(new_df['Date'].values))
print(new_df)

#Create a function to get the buy and the sell signals
def get_signal(data):
    buy_signal = []
    sell_signal = []
    for i in range(len(data['Close'])):
        if data['Close'][i] > data['Upper'][i]:
            buy_signal.append(np.nan)
            sell_signal.append(data['Close'][i])
        elif data['Close'][i] < data['Lower'][i]:
            buy_signal.append(data['Close'][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)

    return(buy_signal,sell_signal)

new_df.loc[:,'Buy'] = get_signal(new_df)[0]
new_df.loc[:,'Sell'] = get_signal(new_df)[1]
#Remove NaN
buy = pd.DataFrame()
buy = new_df.loc[:,'Buy']
sell = pd.DataFrame()
sell = new_df.loc[:,'Sell']

buy.dropna(inplace=True)
sell.dropna(inplace=True)

#plot the data
AAPL[column_list].plot(alpha=0.50, figsize=(12.2, 6.4))
plt.legend(loc='upper left')
plt.title('Bollinger Band for Apple')
plt.ylabel('USD Price ($)')

#plot and shade the area between the two Bollinger bands
#Get the figure
fig = plt.figure(figsize=(12.2, 6.4))
#Add the subpolot
ax = fig.add_subplot(1,1,1)
#get the index values of the data frame
x_axis = pd.to_datetime(new_df.index)
#Plot and shade the area between the upper band and the lower band
ax.fill_between(x_axis, new_df['Upper'],new_df['Lower'],color = 'grey')
#Plot the closing price and the moving average
ax.plot(x_axis,new_df['Close'], color = 'gold', lw = 3, label = 'Close Price')
ax.plot(x_axis,new_df['SMA'], color = 'blue', lw = 3, label = 'Simple Moving Average')
ax.scatter(buy.index, buy, color = 'green', lw = 3, label ='Buy', marker = '^')
ax.scatter(sell.index, sell, color = 'red', lw = 3, label ='Sell', marker = 'v')
#set the title and show the image
ax.set_title('Bollinger Band for Apple')
ax.set_xlabel('Date')
ax.set_ylabel('USD Price ($)')
plt.xticks(rotation=45)
ax.legend()

plt.show()