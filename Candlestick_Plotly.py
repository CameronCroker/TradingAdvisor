#Description: this program will show how to create an interactive candlestick chart in pypthon using python

#iport the libraries
import plotly.graph_objects as go
import pandas as pd

#load the stock data
#store the data
AAPL = pd.read_csv('AAPL.csv')

#Set the date as the index
AAPL = AAPL.set_index(pd.DatetimeIndex(AAPL['Date'].values))

#Give the index a name
AAPL.index.name = 'Date'

#Create the interactive candlestick chart
figure = go.Figure(
    data = [
        go.Candlestick(
            x = AAPL.index,
            low = AAPL['Low'],
            high  = AAPL['High'],
            close = AAPL['Close'],
            open = AAPL['Open'],
            increasing_line_color = 'green',
            decreasing_line_color = 'red'
        )
    ]
)

#figure.update_layout(xaxis_rangeslider_visible = False)

figure.update_layout(
    title = 'Apple price',
    yaxis_title= 'Apple Price USD($)',
    xaxis_title = 'Date'
)

figure.show()