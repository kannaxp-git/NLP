# -*- coding: utf-8 -*-
"""
Book: https://www.safaribooksonline.com/library/view/python-natural-language/9781787121423/
Python Natural Language Processing
@author: sabish
"""
import gensim
import os

workingPath = 'C://Users//sabish//Documents//Courses//TensorFlowDeepLearningProjects//DuplicateQuoraQuestions//'
googleWord2VecFile = 'GoogleNews-vectors-negative300.bin'
os.chdir(workingPath)

w = gensim.models.KeyedVectors.load_word2vec_format(googleWord2VecFile, binary = True)
print('King - man + woman:')
print('')
print (w.most_similar(positive=['woman', 'king'], negative=['man']))


# man:woman is same as king:?
# king - man + woman 
a = 'king'
b = 'man'
c = 'woman'
print (w.most_similar(positive=[a, c], negative=[b])[0])

# aunt:uncle is the same as heiress:
a = 'heiress'
b = 'aunt'
c = 'uncle'
print (w.most_similar(positive=[a, c], negative=[b])[0])

w.doesnt_match("breakfast cereal dinner lunch".split())

w.score(["The fox jumped over a lazy dog".split()])

print('Similarity between man and woman:')
print(w.similarity('woman', 'man'))

