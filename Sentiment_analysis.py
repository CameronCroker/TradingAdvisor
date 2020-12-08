# description: This program predicts if the stock price of a company will increase or decrease based on top news headlines


# description: this program attempts to optimize a users portfolio using Efficient Frontier

#import the libraries
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
plt.style.use('fivethirtyeight')

### import the data ###

#store the data
Value = pd.read_csv('Value_DJIA.csv')
News = pd.read_csv('News_DJIA.csv')

#Show the first three rows of the news


#Merge the data set on the date field
merge = News.merge(Value, how='inner', on='Date', left_index = True)

#Combine all of the news headlines into one column
headlines = []
for row in range(0,len(merge.index)):
    headlines.append(' '.join(str(x) for x in merge.iloc[row, 2:27]))

#print a sample of the combined headlines

#this data set is kinda dirty so lets clean it up
###Clean Data###
clean_headlines = []
for i in range(0, len(headlines)):
    clean_headlines.append(re.sub("b[('\\\")]", '', headlines[i])) #remove b'

#Add the clean headlines to the merge data set
merge['Combined_News'] = clean_headlines
merge.reset_index(inplace=True)
#Show the new column
pd.set_option('display.max_columns',37) ##show all Columns


#Create a function to get the subjectivity
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

#Create a function to get the polarity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

#Create two new columns 'Subjectivity' and 'Polarity'
merge['Subjectivity'] = merge['Combined_News'].apply(getSubjectivity)
merge['Polarity'] = merge['Combined_News'].apply(getPolarity)

#Show the new data columns in the merge data set
#print(merge.head)

#Create a function to get the sentimenet scores
def getSentimentIntensityAnalyzer(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment

#Get the sentiment scores for each day
compound = [] ## a metric that calculates the sums of all the lexicon ratings which have been normalized over (-1,1)
neg = []
pos = []
neu = []
SIA = 0

for i in range (0, len(merge['Combined_News'])):
    SIA = getSentimentIntensityAnalyzer(merge['Combined_News'][i])
    compound.append(SIA['compound'])
    neg.append(SIA['neg'])
    neu.append(SIA['neu'])
    pos.append(SIA['pos'])

#Store the sentiment scores in the merge data set
merge['Compound'] = compound
merge['Negative'] = neg
merge['Neutral'] = neu
merge['Positive'] = pos

#Create a list of columns to keep
keep_columns = ['Open','High', 'Low', 'Volume', 'Subjectivity', 'Polarity', 'Compound', 'Negative', 'Neutral', 'Positive', 'Label']
df = merge[keep_columns]

print(df.head)

#Create the feature data set
X = df
X = np.array(X.drop(['Label'],1))

#Create the data target data
Y  = np.array(df['Label'])

#Split the data into 80% training and 20% testing data sets
x_train,x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

#Create and train the model
model = LinearDiscriminantAnalysis().fit(x_train, y_train)

#Show the models predictions
predictions = model.predict(x_test)
print(predictions)

#Show the model metrics
print(classification_report(y_test, predictions))
