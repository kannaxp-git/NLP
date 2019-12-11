# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:50:53 2017

@author: kach
"""

from nltk import pos_tag
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from math import log
from nltk import word_tokenize
import pyodbc
import re
lemmatizer = WordNetLemmatizer()

from nltk.corpus import wordnet

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN


text="Order something found difficult elsewhere on the site"
clean_sentence=''
for t in pos_tag(word_tokenize(text)):
    clean_sentence=clean_sentence+' '+lemmatizer.lemmatize(t[0],get_wordnet_pos(t[1]))

print(clean_sentence)
    



#DB connection & get data from SQL
con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
#con=pyodbc.connect('DRIVER={SQL Server};Server=dubcpdmsql08;Database=workarea_machinelearing;Trusted_Connection=yes;')
cur=con.cursor()
qry=" select uniquesentenceid as ID, TextForAnalysis from [CUS].[t_GESSSNOW_Normalized] where isvalid=1"
cur.execute(qry)
rows=cur.fetchall()

txt=open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT_KeywordClean.txt","w")

for row in rows:
    sentence= row.TextForAnalysis #sentence = 'errorresolution sharepoint workaround rw'
    sentence=sentence.replace("\t"," ")
    match=re.findall(r'\d+',sentence) #regular expression to find all concatenated string & number e.g office365 7area
    for m in match:
        sentence=sentence.replace(str(m),' '+str(m)+' ')
    
    sentence =sentence.rstrip().lstrip()
        
    clean_sentence=''
    for token in word_tokenize(sentence):
        cleantoken=infer_spaces(token)
        clean_sentence=clean_sentence+' '+cleantoken
        outputstring=''.join([str(row.ID),"\t",clean_sentence,"\n"])
    
    #print(outputstring)
    txt.write(outputstring)
        
        
#        Identifying misspelled/wrongly concatenated strings
#        if token!=cleantoken:
#            outputstring=''.join([token,"\t",cleantoken,"\n"])
#            txt.write(outputstring)

txt.close()
con.commit()
con.close()


#
#print(lemmatizer.lemmatize("licensing",'v'))
#print(lemmatizer.lemmatize("license"))