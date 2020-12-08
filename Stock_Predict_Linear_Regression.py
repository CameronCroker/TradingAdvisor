import numpy as np
import quandl
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

###  this program attempts to address the question:  ###
###   if the 'n' days prior predict future prices?   ###

#get the Stock data
df = quandl.get("WIKI/FB")

#print the data
print(df.head())

#Get the Adjusted Close Price (independent variable)
df = df[['Adj. Close']]

#Take a look at the new data
print(df.head())

# A variable for predicting 'n' days out into the future
forecast_out = 30

#create another column ( the target or dependent variable) shifted 'n' units up
df['Prediction'] = df[['Adj. Close']].shift(-forecast_out)

#Take a look at the new data
print(df.head())
print(df.tail())

### Create the independent data set (X)  ###
#Convert the dataframe to a numpy array
X = np.array(df.drop(['Prediction'], 1))

#Remove the last 'n' rows
X = X[:-forecast_out]

print(X)

### Create the dependent data set (y) ###
#Convert the dataframe to a numpy array (All of the values including the NaN)
y = np.array(df['Prediction'])

#Get all of the y values except the last n rows.
y = y[:-forecast_out]
print(y)

#create the test-train split (80%train, 20% test)
X_train, X_test, y_train,y_test = train_test_split(X, y, test_size=0.2)

# Create and train the Support Vector Machine (Regressor)
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

#train our model
svr_rbf.fit(X_train,y_train)

#Testing Model: Score returns the coefficient of determination R^2 of the prediction
#The best possible score is 1.0
svm_confidence = svr_rbf.score(X_test,y_test)
print ("svm confidence", svm_confidence)

#Create and train the Linear Regression Model
lr = LinearRegression()

#Train the model
lr.fit(X_train,y_train)

#Testing Model: Score returns the coefficient of determination R^2 of the prediction
#The best possible score is 1.0
lr_confidence = lr.score(X_test,y_test)
print ("lr confidence", lr_confidence)

#Set x_forecast equal to the last 30 days of the original data set from Adj. Cllose column
x_forecast = np.array(df.drop(['Prediction'],1))[-forecast_out:]
print(x_forecast)

#print the linear regression predictions for the next 'n' days
lr_prediction = lr.predict(x_forecast)
print(lr_prediction)

#print the SVR predictions for the next 'n' days
svm_prediction = svr_rbf.predict(x_forecast)
print(svm_prediction)