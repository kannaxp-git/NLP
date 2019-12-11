# -*- coding: utf-8 -*-
"""
Source: http://adventuresinmachinelearning.com/gensim-word2vec-tutorial/
@author: sabish
"""
import os
import gensim
from gensim.models import word2vec
import logging
import zipfile
import urllib.request
import numpy as np
from keras.layers import Input, Embedding, merge
from keras.models import Model

workingPath = r'C:\Users\kach\OneDrive\iWorks\Python\SS_AIC_2K18'
os.chdir(workingPath)


def maybe_download(filename, url, expected_bytes):
    """Download a file if not present, and make sure it's the right size."""
    if not os.path.exists(filename):
        filename, _ = urllib.request.urlretrieve(url + filename, filename)
    statinfo = os.stat(filename)
    if statinfo.st_size == expected_bytes:
        print('Found and verified', filename)
    else:
        print(statinfo.st_size)
        raise Exception(
            'Failed to verify ' + filename + '. Can you get to it with a browser?')
    return filename

url = 'http://mattmahoney.net/dc/'
filename = maybe_download('text8.zip', url, 31344016)

sentences = word2vec.Text8Corpus((filename).strip('.zip'))

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = word2vec.Word2Vec(sentences, 
                          iter = 2, # number of epochs  
                          min_count = 10, # minimum word count 
                          size = 300) # embedding dimension 


# get the word vector of "the"
print(model.wv['the'])

# get the most common words
print(model.wv.index2word[0], model.wv.index2word[1], model.wv.index2word[2])

# get the least common words
vocab_size = len(model.wv.vocab)
print(model.wv.index2word[vocab_size - 1], model.wv.index2word[vocab_size - 2], model.wv.index2word[vocab_size - 3])

# find the index of the 2nd most common word ("of")
print('Index of "of" is: {}'.format(model.wv.vocab['of'].index))


# some similarity fun
print(model.wv.similarity('woman', 'man'), model.wv.similarity('man', 'elephant'))

# what doesn't fit?
print(model.wv.doesnt_match("green blue red zebra".split()))
print(model.wv.doesnt_match("green blue sun tree".split()))


# convert the input data into a list of integer indexes aligning with the wv indexes
# Read the data into a list of strings.
def read_data(filename):
    """Extract the first file enclosed in a zip file as a list of words."""
    with zipfile.ZipFile(filename) as f:
        data = f.read(f.namelist()[0]).split()
    return data

def convert_data_to_index(string_data, wv):
    index_data = []
    for word in string_data:
        if word in wv:
            index_data.append(wv.vocab[word].index)
    return index_data

str_data = read_data(filename)
index_data = convert_data_to_index(str_data, model.wv)
print(str_data[:4], index_data[:4])

# convert the wv word vectors into a numpy matrix that is suitable for insertion
# into our TensorFlow and Keras models
vector_dim = 300
embedding_matrix = np.zeros((len(model.wv.vocab), vector_dim))
for i in range(len(model.wv.vocab)):
    embedding_vector = model.wv[model.wv.index2word[i]]
    if embedding_vector is not None:
        embedding_matrix[i] = embedding_vector
        
#### Keras 
valid_size = 16  # Random set of words to evaluate similarity on.
valid_window = 100  # Only pick dev samples in the head of the distribution.
valid_examples = np.random.choice(valid_window, valid_size, replace=False)
# input words - in this case we do sample by sample evaluations of the similarity
valid_word = Input((1,), dtype='int32')
other_word = Input((1,), dtype='int32')
# setup the embedding layer
embeddings = Embedding(input_dim=embedding_matrix.shape[0], output_dim=embedding_matrix.shape[1],
                      weights=[embedding_matrix])
embedded_a = embeddings(valid_word)
embedded_b = embeddings(other_word)
similarity = merge([embedded_a, embedded_b], mode='cos', dot_axes=2)
# create the Keras model
k_model = Model(input=[valid_word, other_word], output=similarity)

def get_sim(valid_word_idx, vocab_size):
    sim = np.zeros((vocab_size,))
    in_arr1 = np.zeros((1,)) 
    in_arr2 = np.zeros((1,))
    in_arr1[0,] = valid_word_idx
    for i in range(vocab_size):
        in_arr2[0,] = i
        out = k_model.predict_on_batch([in_arr1, in_arr2])
        sim[i] = out
    return sim

# now run the model and get the closest words to the valid examples
for i in range(valid_size):
    valid_word = model.wv.index2word[valid_examples[i]]
    top_k = 8  # number of nearest neighbors
    sim = get_sim(valid_examples[i], len(model.wv.vocab))
    nearest = (-sim).argsort()[1:top_k + 1]
    log_str = 'Nearest to %s:' % valid_word
    for k in range(top_k):
        close_word = model.wv.index2word[nearest[k]]
        log_str = '%s %s,' % (log_str, close_word)
    print(log_str)


