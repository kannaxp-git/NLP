# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 23:04:49 2017

@author: kach
"""

from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
#twenty_train.target_names #prints all the categories
#print(twenty_train.data[0:3])
#print("\n".join(twenty_train.data[0].split("\n")[:3])) #prints first line of the first data file
#
from sklearn.feature_extraction.text import CountVectorizer
#count_vect = CountVectorizer()
#X_train_counts = count_vect.fit_transform(twenty_train.data)
##print(X_train_counts)
##print(X_train_counts.shape)
#
from sklearn.feature_extraction.text import TfidfTransformer
#tfidf_transformer = TfidfTransformer()
#X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
#X_train_tfidf.shape
#
from sklearn.naive_bayes import MultinomialNB
#clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),
                     ])
text_clf = text_clf.fit(twenty_train.data, twenty_train.target)

import numpy as np
twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
predicted = text_clf.predict(twenty_test.data)
print(np.mean(predicted == twenty_test.target))