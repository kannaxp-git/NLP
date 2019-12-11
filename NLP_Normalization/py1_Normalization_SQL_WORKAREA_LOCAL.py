import os
my_path = "C:\\Users\\kach\\Documents\\My_Stuff\\MSWorks"
os.chdir(my_path)

import pyodbc
import nltk
import string
import numpy
import pandas
import re
from spacy.en import English
import time
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import sqlalchemy
import urllib
import string

#nltk.data.path.append("C:\\Users\\v-kach\\AppData\\Roaming\\nltk_data")

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']

def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']

def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']

def penn_to_wn(tag):
    if is_adjective(tag):
        return wordnet.ADJ
    elif is_noun(tag):
        return wordnet.NOUN
    elif is_adverb(tag):
        return wordnet.ADV
    elif is_verb(tag):
        return wordnet.VERB
    return wordnet.NOUN

# Input parameters
batchsize = 5000 # Every batchsize number of records will be inserted into DB at once
minAcceptableNumOfChar = 10 # minimum number of characters that define validity of response

start = time.clock()

#Input SQL statements
inputSQL='SELECT [RowID],[SurveyId],[RespondentId],[QuestionId],[Responses],[IsValid] FROM [WORKAREA].[CUS].[t1_ProcessingSurveyData]  WHERE ISVALID=1'
normalizationInputSQL = 'SELECT * FROM [WORKAREA].[CUS].[t_ConfigNormalization] Order by [Order]'
stopwordInputSQL = 'SELECT * FROM [WORKAREA].[CUS].[t_ConfigStopwords]'

# Check validity of Responses inside Script
def response_valid(text):
    text = re.sub(r'[^\w\s]',' ',text) # Remove punctuations
    text = re.sub(' +',' ',text) # Clear extra spaces
    text = text.strip() # Trim string
    numberOfCharacters = len(text) # Calculate number of characters in string

    if (numberOfCharacters <= minAcceptableNumOfChar):
        return "0"
    else:
        return "1"

# Read Map Of Words for normalization
con = pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur = con.cursor()
mapOfWords = pandas.read_sql(normalizationInputSQL, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
mapOfWords = mapOfWords.sort_values('Order', ascending=True)
cur.close()
con.close()

# Read stop words
con = pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur = con.cursor()
stopWords = pandas.read_sql(stopwordInputSQL, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
cur.close()
con.close()

lemmatizer = WordNetLemmatizer()

# Normalize text - This function requires modification and improvements
def clean_text(text):

    for i in range(0,len(mapOfWords)):
        if len(mapOfWords['Original'].iloc[i].split()) <= 1:
            text = re.sub( r'\b'+ mapOfWords['Original'].iloc[i] +'([.,\s]|$)', ' ' + mapOfWords['Map'].iloc[i] + ' ',text, flags=re.IGNORECASE)
        else:
            text = re.sub( r''+ mapOfWords['Original'].iloc[i] +'([.,\s]|$)', ' ' + mapOfWords['Map'].iloc[i] + ' ',text, flags=re.IGNORECASE)
    text = text.strip() # Trim string
    
    return text

# Some extra steps for normalization and removing unnecessary spaces and some improvements of observed issues

nlp = English() # required both for sentence tokenization and lemmatization
nlp.vocab.morphology.lemmatizer.exc[u'verb'][u'need'] = ('need',)
nlp.vocab.morphology.lemmatizer.exc[u'noun'][u'tier'] = ('tier',)
nlp.vocab.morphology.lemmatizer.exc[u'adj'][u'tier'] = ('tier',)

def calling_clean_text(text):
    text = re.sub( '\bcant\b','cannot',text, flags=re.IGNORECASE)
    text = re.sub( 'can\'t','cannot',text, flags=re.IGNORECASE)
    text = re.sub( 'i\'m','I am',text, flags=re.IGNORECASE)
    text = re.sub( 'won\'t','will not',text, flags=re.IGNORECASE)
    text = re.sub( 'n\'t',' not',text, flags=re.IGNORECASE)
    text = re.sub( '\'s','s',text, flags=re.IGNORECASE)
    text = re.sub( '\'ve',' have',text, flags=re.IGNORECASE)
    text = re.sub( '%',' percent ',text)
    text = re.sub(r'[^\w\s](?<![\-.,%\'])',' ',text)
    #text = re.sub(r'\w\s(?<![\-.,])',' ',text)
    remove = string.punctuation
    remove = remove.replace(".", "") # don't remove dots
    remove = remove.replace(",", "") # don't remove commas
    remove = remove.replace("\'", "") # don't remove '
    remove = remove.replace("-", "") # don't remove -
    #text = "".join(l for l in text if l not in remove)
    text = re.sub(' +',' ',text)
    text = clean_text(text)
    text = re.sub(' +',' ',text)
    text = re.sub('Authentication Authentication','Authentication', text) # NEED TO UNDERSTAND WHY THIS HAPPENS AND IMPROVE (need to understand which mapping is causing this issue)
    text = re.sub('Two Factor Authentication Verification','Two Factor Authentication', text) # NEED TO UNDERSTAND WHY THIS HAPPENS AND IMPROVE (reason example for having this later - t2 factors verification)
    
    newdoc = nlp(text)
    newtext = ''
    for token in newdoc:
        if(token.pos_ == 'PUNCT'):
            newtext = newtext + "" + token.lemma_
        else:
            newtext = newtext + " " + str(token)
			#if(str(token.lemma_).lower() == '-pron-'):
            #    newtext = newtext + " " + str(token)
            #else:
            #    newtext = newtext + " " + token.lemma_

    newtext = newtext.strip()

    #pos_tags = nltk.pos_tag(text.split())
    #newtext = ''
    #for word, tag in pos_tags:
    #    word = re.sub(r'[^\w\s]',' ',word)
    #    word = word.strip()
    #    newtext = newtext + " " + lemmatizer.lemmatize(word, penn_to_wn(tag))

    #newtext = newtext.strip()
    return (newtext.lower(), newdoc)


con = pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur = con.cursor()

cur.execute(inputSQL)
rows = cur.fetchall()


mydata = pandas.DataFrame(columns=['UniqueSentenceId','RowID','SurveyId', 'RespondentId', 'NewRespondentId' ,'QuestionId', 'Responses', 'NormalizedResponses', 'IsValid'])
counter  = 0

mytempdata = pandas.DataFrame(columns=['UniqueSentenceId','RowID','SurveyId', 'RespondentId', 'NewRespondentId' ,'QuestionId', 'Responses', 'NormalizedResponses', 'IsValid'])

myNgramdata = pandas.DataFrame(columns=['UniqueSentenceId','SurveyId','QuestionId','RespondentId','NGram', 'Lemma', 'POSTag'])
punctuation = re.compile(r'[-.?!,":;()|0-9]')

uniqueSentenceId = 1
punctuation2 = re.compile(r'["]')
for row in rows:
    s=1
    
    doc = nlp(str(row.Responses))
    sentencesSpacy = [senten.string.strip() for senten in doc.sents]
    if (len(sentencesSpacy) > 1):
        for sent in sentencesSpacy: 
            responseIsValid = response_valid(sent)        
            newResponseId = row.RespondentId + '_' + str(s)
            s=s+1
            newtext, newdoc = calling_clean_text(sent)
            mytempdata.loc[len(mytempdata)] = [uniqueSentenceId, row.RowID, row.SurveyId,row.RespondentId, newResponseId, row.QuestionId, punctuation2.sub("", sent).strip() , '\"' + newtext.strip() + '\"', responseIsValid]
            
            for word in newdoc:
                if ~stopWords["StopWords"].str.contains(str(word).lower()).any() and ~stopWords["StopWords"].str.contains(str(word.lemma_).lower()).any() and ~stopWords["StopWords"].str.contains(punctuation.sub("", str(word)).lower()).any() and punctuation.sub("", str(word)) != '':
                    myNgramdata.loc[len(myNgramdata)] = [uniqueSentenceId, row.SurveyId, row.QuestionId, row.RespondentId, punctuation.sub("", str(word).lower()), punctuation.sub("", str(word.lemma_)), word.pos_]
            uniqueSentenceId = uniqueSentenceId + 1
				

    else:
        responseIsValid = response_valid(str(row.Responses))
        newtext, newdoc = calling_clean_text(str(row.Responses))
        mytempdata.loc[len(mytempdata)] = [uniqueSentenceId, row.RowID, row.SurveyId,row.RespondentId, row.RespondentId, row.QuestionId, punctuation2.sub("", row.Responses).strip() , '\"' + newtext.strip() + '\"', responseIsValid]
        
        for word in newdoc:
                if ~stopWords["StopWords"].str.contains(str(word).lower()).any() and ~stopWords["StopWords"].str.contains(str(word.lemma_).lower()).any() and ~stopWords["StopWords"].str.contains(punctuation.sub("", str(word)).lower()).any() and punctuation.sub("", str(word)) != '':
                    myNgramdata.loc[len(myNgramdata)] = [uniqueSentenceId, row.SurveyId, row.QuestionId, row.RespondentId, punctuation.sub("", str(word).lower()), punctuation.sub("", str(word.lemma_)), word.pos_]
					
        uniqueSentenceId = uniqueSentenceId + 1
					
    #counter = counter + 1
    if (len(mytempdata)%batchsize == 0):
        #mydata = pandas.concat([mydata, mytempdata])
        engine = sqlalchemy.create_engine(
        'mssql+pyodbc:///?odbc_connect=%s' % (
		        urllib.parse.quote(
			        'DRIVER={SQL Server};SERVER=KACH-LAPTOP;'
			        'DATABASE=WORKAREA;Trusted_Connection=yes;')))
        mytempdata.to_sql("t1_ProcessingSurveyData_Normalized", engine, if_exists="append", schema="CUS", index = False)

        engine = sqlalchemy.create_engine(
        'mssql+pyodbc:///?odbc_connect=%s' % (
		        urllib.parse.quote(
			        'DRIVER={SQL Server};SERVER=KACH-LAPTOP;'
			        'DATABASE=WORKAREA;Trusted_Connection=yes;')))
        myNgramdata.to_sql("t1_ProcessingHashTags", engine, if_exists="append", schema="CUS", index = False)		
        del mytempdata
        del myNgramdata
        mytempdata = pandas.DataFrame(columns=['UniqueSentenceId','RowID','SurveyId', 'RespondentId', 'NewRespondentId' ,'QuestionId', 'Responses', 'NormalizedResponses', 'IsValid'])
        myNgramdata = pandas.DataFrame(columns=['UniqueSentenceId','SurveyId','QuestionId','RespondentId','NGram', 'Lemma', 'POSTag'])
   
# if(len(mytempdata) > 0):
    # mydata = pandas.concat([mydata, mytempdata])
  
#mydata.to_csv('file1_Normalization.csv', sep = ',', index = False)
#myNgramdata.to_csv('file1_Hashtag.csv', sep = ',', index = False)

cur.close()
con.close()

engine = sqlalchemy.create_engine(
'mssql+pyodbc:///?odbc_connect=%s' % (
        urllib.parse.quote(
            'DRIVER={SQL Server};SERVER=KACH-LAPTOP;'
            'DATABASE=WORKAREA;Trusted_Connection=yes;')))
mytempdata.to_sql("t1_ProcessingSurveyData_Normalized", engine, if_exists="append", schema="CUS", index = False)

engine = sqlalchemy.create_engine(
'mssql+pyodbc:///?odbc_connect=%s' % (
        urllib.parse.quote(
            'DRIVER={SQL Server};SERVER=KACH-LAPTOP;'
            'DATABASE=WORKAREA;Trusted_Connection=yes;')))
myNgramdata.to_sql("t1_ProcessingHashTags", engine, if_exists="append", schema="CUS", index = False)

print("Processing Finished")
end = 1000 * (time.clock() - start)
print('Time elapsed: %.3f ms' % (end))
