
#reference:  https://medium.com/towards-data-science/machine-learning-nlp-text-classification-using-scikit-learn-python-and-nltk-c52b92a7c73a

from sklearn.datasets import fetch_20newsgroups
twenty_train=fetch_20newsgroups(subset='train',shuffle=True)


##
###twenty_train.target_names #prints all the categories

print(twenty_train.data[1])

print(twenty_train.category[1])

#print(twenty_train.data[1].split("\n")[:5]) #prints first

#print("\n".join(twenty_train.data[1].split("\n")[:5])) #prints first

##
##from sklearn.feature_extraction.text import CountVectorizer
##count_vect = CountVectorizer()
##X_train_counts = count_vect.fit_transform(twenty_train.data)
###X_train_counts.shape
##
##
##from sklearn.feature_extraction.text import TfidfTransformer
##tfidf_transformer = TfidfTransformer()
##X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
###X_train_tfidf.shape
##
##
##from sklearn.naive_bayes import MultinomialNB
##clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
##
##from sklearn.pipeline import Pipeline
##text_clf = Pipeline([('vect', CountVectorizer()),('tfidf',TfidfTransformer()),('clf',MultinomialNB()),])
##
##text_clf = text_clf.fit(twenty_train.data, twenty_train.target)
##
##import numpy as np
##twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
##predicted = text_clf.predict(twenty_test.data)
##print(predicted)
###print(np.mean(predicted == twenty_test.target))
##
##                    
