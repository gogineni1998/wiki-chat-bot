import nltk

from nltk.corpus import stopwords
import re
import pandas as pd
import pickle

df = pd.read_csv('topics.csv')
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')


STOPWORDS = set(stopwords.words('english'))
def clean_text(text):
    text = text.lower()
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

df['topic_description'] = df['topic_description'].apply(clean_text)

df = df.sample(frac = 1)
print(df.head())
print(df.tail())
from sklearn.model_selection import train_test_split
X = df.topic_description
y = df.topic
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 42)

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer

lr = Pipeline([('vect', CountVectorizer()),
               ('tfidf', TfidfTransformer()),
               ('clf', LogisticRegression()),
              ])

print("Training Started : ")
lr.fit(X_train,y_train)

pickle.dump(lr, open('logistic_regression.pkl', 'wb'))