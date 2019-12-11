# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 01:06:58 2018

@Reference: https://nlpforhackers.io/topic-modeling/
@Reference (internal): C:\Users\kach\OneDrive\iWorks\Python\NLP_IE_TopicModeling\NLP_ScikitLearn_topicModeling.py
@author: kach
"""

#Using Scikit-Learn for Topic Modeling
from nltk.corpus import brown
 
data = []
 
for fileid in brown.fileids():
    document = ' '.join(brown.words(fileid))
    data.append(document)
 
NO_DOCUMENTS = len(data)
print(NO_DOCUMENTS)
#print(data[:5])


from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
 
NUM_TOPICS = 10
 
vectorizer = CountVectorizer(min_df=5, max_df=0.9, 
                             stop_words='english', lowercase=True, 
                             token_pattern='[a-zA-Z\-][a-zA-Z\-]{2,}')
data_vectorized = vectorizer.fit_transform(data)
 
# Build a Latent Dirichlet Allocation Model
lda_model = LatentDirichletAllocation(n_topics=NUM_TOPICS, max_iter=10, learning_method='online')
lda_Z = lda_model.fit_transform(data_vectorized)
#print(lda_Z.shape)  # (NO_DOCUMENTS, NO_TOPICS)
 
# Build a Non-Negative Matrix Factorization Model
nmf_model = NMF(n_components=NUM_TOPICS)
nmf_Z = nmf_model.fit_transform(data_vectorized)
#print(nmf_Z.shape)  # (NO_DOCUMENTS, NO_TOPICS)
 
# Build a Latent Semantic Indexing Model
lsi_model = TruncatedSVD(n_components=NUM_TOPICS)
lsi_Z = lsi_model.fit_transform(data_vectorized)
#print(lsi_Z.shape)  # (NO_DOCUMENTS, NO_TOPICS)
 
 
# Let's see how the first document in the corpus looks like in different topic spaces
#print(lda_Z[0])
#print(nmf_Z[0])
#print(lsi_Z[0])


def print_topics(model, vectorizer, top_n=10):
    for idx, topic in enumerate(model.components_):
        print("Topic %d:" % (idx))
        print([(vectorizer.get_feature_names()[i], topic[i])
                        for i in topic.argsort()[:-top_n - 1:-1]])
 
print("LDA Model:")
print_topics(lda_model, vectorizer)
print("=" * 20)
 
print("NMF Model:")
print_topics(nmf_model, vectorizer)
print("=" * 20)
 
print("LSI Model:")
print_topics(lsi_model, vectorizer)
print("=" * 20)




##--------------------------------------------------------------
##Document similarity
##Transforming an unseen document goes like this:
#text = "The economy is working better than ever"
#x = nmf_model.transform(vectorizer.transform([text]))[0]
#print(x)
# 
##Here’s how to implement the similarity functionality we’ve seen in the gensim section:
#
#from sklearn.metrics.pairwise import euclidean_distances
# 
#def most_similar(x, Z, top_n=5):
#    dists = euclidean_distances(x.reshape(1, -1), Z)
#    pairs = enumerate(dists[0])
#    most_similar = sorted(pairs, key=lambda item: item[1])[:top_n]
#    return most_similar
# 
#similarities = most_similar(x, nmf_Z)
#document_id, similarity = similarities[0]
#print(data[document_id][:1000])
##----------------------------------------------------------------