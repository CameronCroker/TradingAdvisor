#selecting the best portfolio set based on some target function

#import the libraries
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_datareader import data as web
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

plt.style.use('fivethirtyeight')

#Get the stock symbols/tickers in the portfolio
#FAANG

assets = ['FB', 'AMZN','AAPL','NFLX','GOOG']

#assign weights to the stocks.
weights = np.array([0.2,0.2,0.2,0.2,0.2])

#Get the portfolio start date (for the first full year of facebook)
start = dt.datetime(2013,1,1)
today = dt.datetime.today().strftime('%Y-%m-%d')
end = dt.datetime(2016,1,1)

#Create a dataframe to store the adjusted close price of the stocks
df = pd.DataFrame()

#Store the adjusted close price of the stock in the df
for stock in assets:
    df[stock] = web.DataReader(stock, data_source='yahoo', start = start, end = end)['Adj Close']


#visually show the portfolio
title = 'Portfolio Adj. Close Price History'

#Get the Stocks
my_stocks = df

#Create and plot the graph
for c in my_stocks.columns.values:
    plt.plot(my_stocks[c], label = c)

plt.title(title)
plt.xlabel('Date', fontsize = 18)
plt.ylabel('Adj. Price USD ($)',fontsize = 18)
plt.legend(my_stocks.columns.values,loc = 'upper left')


#Show the daily simple rerun, percentage change
returns = df.pct_change()

#Create and show the annualized covariance matrix
cov_matrix_annual = returns.cov() * 252

#Calculate the portfolio varaicne
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))

#Calculate the portfolio volatility aka standard deviation
port_volatility = np.sqrt(port_variance)
print(port_variance)

#Calculate the annual portfolio return
portfolioSimpleAnnualReturn = np.sum(returns.mean()* weights)*252

#Show the expected annual return, volatility (risk), and variance
percent_var= str(round(port_variance,2)*100) + '%'
percent_vol = str(round(port_volatility, 2) * 100) + '%'
percent_ret = str(round(portfolioSimpleAnnualReturn,2) *100)+ '%'

print('Expected annual return: ' + percent_ret)
print('Annual volatility / risk: ' + percent_vol)
print('Annual Variance ' + percent_var)

#Portfolio Optimization1

#Caluclate the expected returns and the annalised sample covariance matrix of asset returns
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

#optimize for max sharpe ratio (vs risk-free)
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
print(cleaned_weights)
ef.portfolio_performance(verbose = True)



#Discrete Allocation Algorithm
latest_prices = get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=15000)


allocation, leftover = da.lp_portfolio()
print('Discrete Allocation: ', allocation)
print('Funds Remaining: ${:.2f}: '.format(leftover))
