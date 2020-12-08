# description: this program uses the money flow index to determine whe to buy and sell stocks

#import the libraries
import warnings
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_datareader import data
plt.style.use('fivethirtyeight')
warnings.filterwarnings('ignore')

#Get the data
#To do: format these to be only the dates from a specific date range
AAPL = pd.read_csv('AAPL.csv')

#Set the  index
AAPL = AAPL.set_index(pd.DatetimeIndex(AAPL['Date'].values))

print(AAPL)

#Visually show the data
plt.figure(figsize=(12.5,4.5))
plt.plot(AAPL['Close'], label = 'Close Price')
plt.title('Apple close price')
plt.xlabel('Date')
plt.ylabel('Close price USD ($)')
plt.legend(AAPL.columns.values, loc='upper left')

#Calculaate the typical price
typical_price = (AAPL['Close'] + AAPL['High'] + AAPL['Low'] )/3
typical_price

#Get the period typically MFI uses a preiod of 14 days
period = 14

#Calculate the money flow
money_flow = typical_price * AAPL['Volume']
print(money_flow)

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

#create the MFI dataframe
df2 = pd.DataFrame()
df2['MFI'] = mfi

#visually show the MFI
plt.figure(figsize=(12.5,4.5))
plt.plot(df2['MFI'], label = 'MFI')
plt.title('MFI')
plt.axhline(10, linestyle = '--', color = 'orange')
plt.axhline(20, linestyle = '--', color = 'blue')
plt.axhline(80, linestyle = '--', color = 'blue')
plt.axhline(90, linestyle = '--', color = 'orange')
plt.ylabel('MFI Values')

#Create a new data frame
new_df = pd.DataFrame()
new_df = AAPL[period:]
new_df['MFI'] = mfi

# Create a function to get the buy and sell signals
def get_signal(data,high, low):
    buy_signal = []
    sell_signal = []

    for i in range (len(data['MFI'])):
        if data['MFI'][i] > high:
            buy_signal.append(np.nan)
            sell_signal.append(data['Close'][i])
        elif data['MFI'][i] < low:
            buy_signal.append(data['Close'][i])
            sell_signal.append(np.nan)
        else:
            buy_signal.append(np.nan)
            sell_signal.append(np.nan)

    return(buy_signal,sell_signal)

#Add new column (Buy & Sell
new_df['Buy'] = get_signal(new_df,80,20)[0]
new_df['Sell'] = get_signal(new_df,80,20)[1]

#Show the data

#plot the data
plt.figure(figsize=(12.5,4.5))
plt.title('MFI')
plt.plot(AAPL['Close'], label = 'Close Price', alpha = 0.5)
plt.scatter(new_df.index, new_df['Buy'], color ='green', label='Buy Signal', marker = '^', alpha = 1)
plt.scatter(new_df.index, new_df['Sell'], color ='red', label='Sell Signal', marker = 'v', alpha = 1)
plt.title('Apple close price')
plt.xlabel('Date')
plt.ylabel('Close price USD ($)')
plt.legend(loc='upper left')


print(new_df)

plt.show()
