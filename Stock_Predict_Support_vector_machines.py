#Description: this program predicts the price of FB stock for a specific Day

#import the libraries
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#store the data
TSLA = pd.read_csv('TSLA.csv')

#Set the date as the index
TSLA = TSLA.set_index(pd.DatetimeIndex(TSLA['Date'].values))

# Get and print the last row of data
TSLA = TSLA[['Adj Close']]

#prepare the data for training the SVR models
#Get all of the data except for the last row

# A variable for predicting 'n' days out into the future
forecast_out = 30

#create another column ( the target or dependent variable) shifted 'n' units up
TSLA['Prediction'] = TSLA[['Adj Close']].shift(-forecast_out)

#Take a look at the new data
print(TSLA.head())
print(TSLA.tail())

### Create the independent data set (X)  ###
#Convert the dataframe to a numpy array
X = np.array(TSLA.drop(['Prediction'], 1))

#Remove the last 'n' rows
X = X[:-forecast_out]

print(X)

### Create the dependent data set (y) ###
#Convert the dataframe to a numpy array (All of the values including the NaN)
y = np.array(TSLA['Prediction'])

#Get all of the y values except the last n rows.
y = y[:-forecast_out]
print(y)

### Create the 3 support Vector Regression Models ###
#create the test-train split (80%train, 20% test)
X_train, X_test, y_train,y_test = train_test_split(X, y, test_size=0.2)

###Linear###
#Create and train a SVR model using a linear kernal
svr_lin = SVR(kernel='linear', C=1000.0)
svr_lin.fit(X_train,y_train)

lin_confidence = svr_lin.score(X_test,y_test)
print ("lin confidence", lin_confidence)

###Polynomial###
#Create and train a SVR model using a Polynomial kernal
svr_poly = SVR(kernel='poly', C=1000.0, degree=2)
svr_poly.fit(X_train,y_train)

poly_confidence = svr_poly.score(X_test,y_test)
print ("Polynomial confidence", poly_confidence)

###SVR###
# Create and train the Support Vector Machine (Regressor)
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

#train our model
svr_rbf.fit(X_train,y_train)

#Testing Model: Score returns the coefficient of determination R^2 of the prediction
#The best possible score is 1.0
rbf_confidence = svr_rbf.score(X_test,y_test)
print ("RBF confidence", rbf_confidence)

rbf_predict = svr_rbf.predict(X_test)
lin_predict = svr_lin.predict(X_test)
poly_predict = svr_poly.predict(X_test)

plt.figure(figsize=(16,8))
plt.scatter(X_train,y_train, color='red',label='Data')
plt.scatter(X_test,rbf_predict, color = 'green', label = 'RBF Model')
plt.scatter(X_test,lin_predict, color = 'blue', label = 'Linear Model')
plt.scatter(X_test,poly_predict, color = 'black', label = 'Polynomial Model')
plt.legend(loc = 'upper right')
plt.show()

