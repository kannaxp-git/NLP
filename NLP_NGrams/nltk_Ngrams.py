##------USING NLTK NGARAMS -----------
#from nltk import ngrams
#sentence = 'Better understanding of products and current Microsoft services'
#n = 3
#sixgrams = ngrams(sentence.split(), n)
#for grams in sixgrams:
#  print(grams)
#

#-------- using SCIKIT LEARN -----------
#from sklearn.feature_extraction.text import CountVectorizer
##vectorizer= CountVectorizer()
## 
#corpus=[
#        'This is the first document',
#        'this is the second document',
#        'and the third one',
#        'Is this the first document?',
#        'kannan kannan']
##  
##x=vectorizer.fit_transform(corpus)
##print(x)
##print(vectorizer.get_feature_names())
##print(x.toarray())
##print(vectorizer.vocabulary_.get('kannan'))
#
#bigram_vectorizer=CountVectorizer(ngram_range=(1,3),token_pattern=r'\b\w+\b', min_df=1)
#analyze=bigram_vectorizer.build_analyzer()
#x=analyze(corpus[0])
#print(x)


#---------------NLTK Ngram -----------------
import nltk
from nltk.util import ngrams
from collections import Counter
#import os

import pyodbc
con = pyodbc.connect('DRIVER={SQL Server};Server=kach-laptop;Database=workarea;Trusted_Connection=yes;')
cur = con.cursor()
#cur.execute('select cast((subject+' '+ Description_cleaned) as varchar(MAX)) as txt from mst.t_Sample where description_cleaned is not null')
cur.execute('select cast(Description_Normalized_StopWords as varchar(MAX)) as txt from mst.t_Sample where Description_Normalized_StopWords is not null')
rows = cur.fetchall()


txtinput=open("C:\\Users\\kach\\Desktop\\Temp\\Ngram_input.txt","w",encoding="utf8")
txtoutput=open("C:\\Users\\kach\\Desktop\\Temp\\Ngram_Output1.txt","w",encoding="utf8")

#text = "I need to write a program in NLTK that breaks a corpus (a large collection of txt files) into unigrams, bigrams, trigrams, fourgrams and kannan kannan fivegrams.I need to write a program in NLTK that breaks a corpus kannan kannan kannan"
#text=' '.join(corpus)\
for row in rows:
    txtinput.write(row.txt)

f=open("C:\\Users\\kach\\Desktop\\Temp\\Ngram_input.txt",encoding="utf8")
raw=f.read()

N=1 #to mention number of grams
MinFreq=500

token = nltk.word_tokenize(raw)
bigrams = ngrams(token,N)
#trigrams = ngrams(token,3)
#fourgrams = ngrams(token,4)
#fivegrams = ngrams(token,5)

grams=Counter(bigrams).items()
#grams=Counter(bigrams)
#grams=dict(grams)

#print(Counter(bigrams))

for g in grams:
    if g[1]>=MinFreq:
        outputstring=''.join(str(g[0])+"\t"+str(g[1])+"\n")
        txtoutput.write(outputstring)

txtinput.close()
#os.remove("C:\\Users\\kach\\Desktop\\Temp\\Ngram_input.txt")
txtoutput.close()
