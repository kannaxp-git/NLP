# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 01:06:56 2018

@author: kach

ref: https://nlpforhackers.io/named-entity-extraction/

"""

#NLTK NER Chunker
#NLTK has a standard NE annotator so that we can get started pretty quickly.

def NER_spacy(sentence):
    import spacy
    nlp=spacy.load('en')  #install 'en' model (python 3 -m spacy download en)
    doc=nlp(sentence)
    print('name Entity: {0}'.format(doc.ents))


def NER_nltk(sentence):
    
    from nltk import word_tokenize, pos_tag, ne_chunk
    from nltk.chunk import conlltags2tree, tree2conlltags
    
    ne_tree = ne_chunk(pos_tag(word_tokenize(sentence)))
    print(ne_tree)
    
    print("-----------------------------")
    
    iob_tagged = tree2conlltags(ne_tree)
    print(iob_tagged)
    
    print("-----------------------------")
    
    ne_tree = conlltags2tree(iob_tagged)
    print(ne_tree)

    
    

if __name__=='__main__':
    sentence = "Mark and John are working at Microsoft they used to play football since school days. Mark is planning to do his masters"
    
#    NER_nltk(sentence)
    NER_spacy(sentence)
 
