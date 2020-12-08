#Description: This is a python program for finance
#             This program will show you simple returns, Daily Returns and Volatility

#import the libraries
import datetime as dt
import numpy as np
import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the stock symbols for the portfolio
#We are going to use FAANG
assets = ['FB', 'AMZN','AAPL','NFLX','GOOG']

# Get the portfolio start date (for the first full year of facebook)
start = dt.datetime(2013,1,1)
today = dt.datetime.today().strftime('%Y-%m-%d')
end = dt.datetime(2016,1,1)

# Create a dataframe to store the adjusted close price of the stocks
df = pd.DataFrame()

# Get the number of assets in the portfolio
numAssets = len(assets)
print('you have '+str(numAssets) + ' assets in your porfolio')


# Store the adjusted close price of the stock in the df
def get_my_portfolio(stocks=assets, start=start, end=end,col='Adj Close'):
    data = web.DataReader(stocks, data_source='yahoo', start=start, end=end)['Adj Close']
    return data


# Get the stock Portfolio Adj. Close Price
my_stocks = get_my_portfolio(assets)

#Create a function to visualize the portfolio
def show_graph(stocks = assets, start = start, end = end, col = 'Adj Close'):

    #Create a title for the portfolio
    title = 'Portfolio ' + col + ' Price History'

    #Get the stocks
    my_stocks = get_my_portfolio(stocks, start = start, end = end, col = col)

    #give the figure size
    plt.figure(figsize=(12.2, 4.5))

    #loop through each stock and plot the price
    for c in my_stocks.columns.values:
        plt.plot(my_stocks[c], label = c)

    plt.title(title)
    plt.xlabel('Date', fontsize= 18)
    plt.ylabel(col + ' Price USD ($)', fontsize = 18)
    plt.legend(my_stocks.columns.values, loc = 'upper left')

    plt.show()

#show the adjusted closed price for FAANG
#show_graph(assets)

#Calculate the simple returns
daily_simple_returns = my_stocks.pct_change(1)

#show the daily simple returns
print(daily_simple_returns)

#show the stock correlation
print(daily_simple_returns.corr())

#Show the covariance matrix for simple returns
print(daily_simple_returns.cov())

#Show the Variance
print(daily_simple_returns.var())

#Print the standard deviation for daily simple returns
print('The Stock Volatility: ')
print(daily_simple_returns.std())

#visualize the stocks daily simple returns / Volatility
plt.figure(figsize=(12.2,4.5))

#loop through each stock and plot the simple returns
for c in daily_simple_returns.columns.values:
    plt.plot(daily_simple_returns.index, daily_simple_returns[c], lw=2, label = c)

#Create a legend
plt.legend(loc= 'upper right', fontsize = 10)
plt.title('Volatility')
plt.xlabel('Date')
plt.ylabel('Daily simple returns')


#show the mean of the daily simple returns
daily_mean_simple_returns = daily_simple_returns.mean()
print('The mean daily simple returns: ')
print(daily_mean_simple_returns)

#Calculate the expected portfolio daily returns
randomWeights = np.array([0.4,0.1,0.3,0.1,0.1]) #40% FB, 10% AMZN, 30% AAPL, 10% NFLX, 10% GOOG
portfolioSimpleReturn = np.sum(daily_mean_simple_returns * randomWeights)

#Print the expected portfolio returns
print('the daily expected portfolio return : ' + str(portfolioSimpleReturn))

#Get the yearly simple return
print('Expected annualised portfolio simple return: ' + str(portfolioSimpleReturn * 253))

#Calculate the growth of the investment (accumulative returns)
# (period_1 + 1) * (period_2 + 1) * ..* (period_n +1)
daily_Cum_simple_return = (daily_simple_returns + 1).cumprod()
#show the cum simple returns
print(daily_Cum_simple_return)

#visualize the daily cumulative simple returns
plt.figure(figsize = (12.2, 4.5))

for c in daily_Cum_simple_return.columns.values:
    plt.plot(daily_Cum_simple_return.index, daily_Cum_simple_return[c],lw = 2, label = c)

plt.legend(loc = 'upper left', fontsize = 10)
plt.xlabel('Date')
plt.ylabel('Growth of $1 investment')
plt.title('Daily Cumulative simple returns')
plt.show()
