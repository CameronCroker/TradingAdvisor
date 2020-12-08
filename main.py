import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pandas_datareader import data as web
plt.style.use('fivethirtyeight')

#store the data
words = open('words.txt').read().splitlines()



#have a quick scquiz
for i in range(0, 50):
    print(words[i])