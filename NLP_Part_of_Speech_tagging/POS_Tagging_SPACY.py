# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 21:07:21 2017

@author: kach
"""

from spacy.en import English
parser=English()

sentence="There is an art, it says, or rather, a knack to flying."
parsedData=parser(sentence)
for i,token in enumerate(parsedData):
    print("original:", token.orth, token.orth_)
    print("lowercased:", token.lower, token.lower_)
    print("lemma:", token.lemma, token.lemma_)
    print("shape:", token.shape, token.shape_)
    print("prefix:", token.prefix, token.prefix_)
    print("suffix:", token.suffix, token.suffix_)
    print("log probability:", token.prob)
    print("Brown cluster id:", token.cluster)
    print("----------------------------------------")

#import spacy
#nlp = spacy.load('en')
#doc = nlp(u'They told us to duck.')
#for word in doc:
#    print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)