# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 09:50:53 2017

@author: kach
"""

from nltk import pos_tag
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import pyodbc
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


#DB connection & get data from SQL
con=pyodbc.connect('DRIVER={SQL Server};Server=dubcpdmsql08;Database=WORKAREA_KANNAN;Trusted_Connection=yes;')
#con=pyodbc.connect('DRIVER={SQL Server};Server=dubcpdmsql08;Database=workarea_machinelearing;Trusted_Connection=yes;')
cur=con.cursor()
qry=" select uniqueidentifier as ID, cast(english_comment as varchar(MAX)) as TextForAnalysis from  [CPE].[CPE_SurveyMasterData]"
cur.execute(qry)
rows=cur.fetchall()

txt=open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT_KeywordClean.txt","w")

for row in rows:
    sentence= row.TextForAnalysis #sentence = 'errorresolution sharepoint workaround rw'
    sentence=sentence.replace("\t"," ")
    sentence =sentence.rstrip().lstrip()
        
    clean_sentence=''
    for token in pos_tag(word_tokenize(sentence)):
        if len(token[0])>1:
            clean_sentence=clean_sentence+' '+lemmatizer.lemmatize(token[0],get_wordnet_pos(token[1]))
            outputstring=''.join([str(row.ID),"\t",clean_sentence,"\n"])
    
    print(row.ID)
    txt.write(outputstring)
    
txt.close()
con.commit()
con.close()
