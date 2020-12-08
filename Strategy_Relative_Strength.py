#Description: Use the relative Strength Index (RSI) and python to determine if a stock is being over bought or over sold

#import the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


#store the data
MSFT = pd.read_csv('MSFT.csv')

#Set the date as the index
MSFT = MSFT.set_index(pd.DatetimeIndex(MSFT['Date'].values))

#Give the index a name
MSFT.index.name = 'Date'

#visualize the data (implement a date range function)
plt.figure(figsize=(12.2, 4.5))
plt.plot(MSFT.index, MSFT['Adj Close'], label = 'Adj Close')
plt.title('Adj. Close Price History')
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Adj Close price USD ($)', fontsize = 18)



#prepare the data to calculate the RSI

#Get the Difference in price from the previous day

delta = MSFT['Adj Close'].diff(1)


#Get rid of NaN
delta = delta.dropna()

print(delta)


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

#Show the RSI Visually
plt.figure(figsize=(12.2,4.5))
RSI.plot()

#put it all together

#Create a new data frame

new_df = pd.DataFrame()

new_df['Adj Close'] = MSFT['Adj Close']
new_df['RSI'] = RSI

print(new_df)


#Visually show the adjusted close price and RSI
#Plot the adjusted close price
plt.figure(figsize=(12.2, 4.5))
plt.plot(new_df.index, new_df['Adj Close'])
plt.title('Adj Close price history')
plt.legend(new_df.columns.values, loc='upper left')

#Plot the corresponding RSI Values and the significat levels
plt.figure(figsize=(12.2,4.5))
plt.plot(new_df.index,new_df['RSI'])
plt.axhline(0,linestyle = '--', alpha = 0.5, color= 'grey')
plt.axhline(10,linestyle = '--', alpha = 0.5, color= 'orange')
plt.axhline(20,linestyle = '--', alpha = 0.5, color= 'green')
plt.axhline(30,linestyle = '--', alpha = 0.5, color= 'red')
plt.axhline(70,linestyle = '--', alpha = 0.5, color= 'red')
plt.axhline(80,linestyle = '--', alpha = 0.5, color= 'green')
plt.axhline(90,linestyle = '--', alpha = 0.5, color= 'orange')
plt.axhline(100,linestyle = '--', alpha = 0.5, color= 'grey')


plt.show()