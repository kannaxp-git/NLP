# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 23:31:57 2018

@author: kach
"""

import nltk
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

text = """I need to write a program in NLTK that breaks a corpus (a large collection of \
txt files) into unigrams, bigrams, trigrams, fourgrams and fivegrams.\ 
I need to write a program in NLTK that breaks a corpus"""
token = nltk.word_tokenize(text)
bigrams = ngrams(token,2)
trigrams = ngrams(token,3)
fourgrams = ngrams(token,4)
fivegrams = ngrams(token,5)

print(Counter(bigrams))