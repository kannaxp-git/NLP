####
"""
@author: Kannan Chandrasekaran (kach@microsoft.com)

Google's pre-trained model: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
http://w3cgeek.com/how-to-calculate-the-sentence-similarity-using-word2vec-model-of-gensim-with-python.html
"""
       
import numpy as np
import gensim
from scipy import spatial
w2v_model=gensim.models.KeyedVectors.load_word2vec_format(r'C:\Users\kach\Downloads\GoogleNews-vectors-negative300.bin', binary=True)

def avg_feature_vector(words, model, num_features):
        #function to average all words vectors in a given paragraph
        featureVec = np.zeros((num_features,), dtype="float32")
        nwords = 0

        #list containing names of words in the vocabulary
        index2word_set = set(model.index2word) #this is moved as input param for performance reasons
        for word in words:
            if word in index2word_set:
                nwords = nwords+1
                featureVec = np.add(featureVec, model[word])

        if(nwords>0):
            featureVec = np.divide(featureVec, nwords)
        return featureVec
    
#get average vector for sentence 1
sentence_1 = "slow"
sentence_1_avg_vector = avg_feature_vector(sentence_1.split(), model=w2v_model, num_features=300)

#get average vector for sentence 2
sentence_2 = "device performance"
sentence_2_avg_vector = avg_feature_vector(sentence_2.split(), model=w2v_model, num_features=300)

sen1_sen2_similarity =  1 - spatial.distance.cosine(sentence_1_avg_vector,sentence_2_avg_vector)
print(sen1_sen2_similarity)

