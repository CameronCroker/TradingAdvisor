#Description: This function retrieves data from Quandl and writes it to a csv (input: String)

import quandl
import numpy as np
import pandas as pd


def create_csv(ticker):
    keyfile = open('Quandl API Key', 'r')
    API_KEY = keyfile.readline().rstrip()

    #To-Do implement type check (type=str, ticker)
    data = quandl.get('WIKI/' + ticker)
    df = pd.DataFrame(data)
    df.to_csv(ticker + '.csv')
