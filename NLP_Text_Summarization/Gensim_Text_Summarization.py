from numpy._distributor_init import NUMPY_MKL
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.summarization import summarize

##text = "Thomas A. Anderson is a man living two lives. By day he is an " + \
##    "average computer programmer and by night a hacker known as " + \
##    "Neo. Neo has always questioned his reality, but the truth is " + \
##    "far beyond his imagination. Neo finds himself targeted by the " + \
##    "police when he is contacted by Morpheus, a legendary computer " + \
##    "hacker branded a terrorist by the government. Morpheus awakens " + \
##    "Neo to the real world, a ravaged wasteland where most of " + \
##    "humanity have been captured by a race of machines that live " + \
##    "off of the humans' body heat and electrochemical energy and " + \
##    "who imprison their minds within an artificial reality known as " + \
##    "the Matrix. As a rebel against the machines, Neo must return to " + \
##    "the Matrix and confront the agents: super-powerful computer " + \
##    "programs devoted to snuffing out Neo and the entire human " + \
##    "rebellion. "

#print('Input text:')
#print(text)

#print ('Summary:')
#print (summarize(text))

#print (summarize(text, split=True))

#print(summarize(text, ratio=0.5))

#print(summarize(text,word_count=50))

from gensim.summarization import keywords
#print('Keywords:')
#print(keywords(text))


import io
import operator
sample_file=io.open("C:\\Users\\kach\\Desktop\\Temp\\CPE_H2ManagedQ3.txt",'r',encoding="iso-8859-1")
text=sample_file.read()
#print(text)
#print ('Summary:')
print(summarize(text))
#print(summarize(text, ratio=0.1))


##print ('\nKeywords:')
##print(keywords(text))
