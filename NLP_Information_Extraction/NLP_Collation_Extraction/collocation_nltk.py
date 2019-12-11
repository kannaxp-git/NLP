#http://www.nltk.org/howto/collocations.html
#https://radimrehurek.com/gensim/models/phrases.html

import nltk
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()
finder = BigramCollocationFinder.from_words(
    nltk.corpus.genesis.words('english-web.txt'))
print(finder.nbest(bigram_measures.pmi,10))
 
