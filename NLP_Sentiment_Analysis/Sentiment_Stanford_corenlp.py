# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 14:53:51 2018

@author: kach
#reference: https://stackoverflow.com/questions/32879532/stanford-nlp-for-python


Created on Tue Dec 12 18:04:09 2017

Stanford NLP download:
    https://stanfordnlp.github.io/CoreNLP/download.html

Py-coreNLP:
    https://github.com/smilli/py-corenlp

server Instructions:
    https://stanfordnlp.github.io/CoreNLP/corenlp-server.html#getting-started
    
    
    STARTING: (POWERSHELL)
        NAVIAGATE TO: C:\ANACONDA3\STANFORD-CORENLP\
        java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000
    
    STOPPING:
        CTRL-C
        
		important: 64 bit JAVA is mandatory. or else server start command will throw out of memory error
        
"""

from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')
res = nlp.annotate("I love you. I hate him. You are nice. He is dumb. too much informations.",
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 10000,
                   })
for s in res["sentences"]:
    print("%d: '%s': %s %s" % (
        s["index"],
        " ".join([t["word"] for t in s["tokens"]]),
        s["sentimentValue"], s["sentiment"]))