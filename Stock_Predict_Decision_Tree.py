#Description: this program uses a machine learning algorithm called
#of a stock will increase or decrease



#import the libraries
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


#store the data
AAPL = pd.read_csv('AAPL.csv')

#Set the date as the index
AAPL = AAPL.set_index(pd.DatetimeIndex(AAPL['Date'].values))

#Give the index a name
AAPL.index.name = 'Date'

#Manipulate the data
#Create the target column
AAPL['Price_up'] = np.where(AAPL['Close'].shift(-1) > AAPL['Close'],1,0)

#remove the data column
AAPL = AAPL.drop(columns=['Date'])

#split the data set into a feature data set and a target data set
X = AAPL.iloc[:,0:AAPL.shape[1]-1].values
Y = AAPL.iloc[:,AAPL.shape[1]-1].values

#Split the data again but this time into 80% training and 20% testing data sets
X_train,X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2)

#Create and train the model (DecisionTreeClassifier)
tree = DecisionTreeClassifier().fit(X_train,Y_train)

#Show how well the model did on the test data set
print(tree.score(X_test,Y_test))

#Show the models predictions
tree_predictions = tree.predict((X_test))
print('Predicted Values: ', tree_predictions,'Actual Values: ', Y_test)


