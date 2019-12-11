import os
my_path = "C:\\Users\\kach\\Desktop\\Temp"
os.chdir(my_path)

import pyodbc
import string
import pandas
import re
##from spacy.en import English

#nltk.data.path.append("C:\\Users\\v-kach\\AppData\\Roaming\\nltk_data")


# Input parameters
minAcceptableNumOfChar = 10 # minimum number of characters that define validity of response


#Input SQL statements
#'SELECT [RowID],[Responses] FROM [WORKAREA].[CUS].[t1_ProcessingSurveyData]  WHERE ISVALID=1'
normalizationInputSQL = 'SELECT * FROM [WORKAREA].[MST].[t_ConfigNormalization]  Order by [Order]'
stopwordInputSQL = 'SELECT * FROM [WORKAREA].[MST].[t_ConfigStopwords]'

# Read Map Of Words for normalization
con = pyodbc.connect('DRIVER={SQL Server};Server=KACH_SAW;Database=WORKAREA;Trusted_Connection=yes;')
cur = con.cursor()
mapOfWords = pandas.read_sql(normalizationInputSQL, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
mapOfWords = mapOfWords.sort_values('Order', ascending=True)
cur.close()
con.close()

# Read stop words
con = pyodbc.connect('DRIVER={SQL Server};Server=KACH_SAW;Database=WORKAREA;Trusted_Connection=yes;')
cur = con.cursor()
stopWords = pandas.read_sql(stopwordInputSQL, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
cur.close()
con.close()

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

# Normalize text - This function requires modification and improvements
def clean_text(text):

    for i in range(0,len(mapOfWords)):
        if len(mapOfWords['Original'].iloc[i].split()) <= 1:
            text = re.sub( r'\b'+ mapOfWords['Original'].iloc[i] +'([.,\s]|$)', ' ' + mapOfWords['Map'].iloc[i] + ' ',text, flags=re.IGNORECASE)
        else:
            text = re.sub( r''+ mapOfWords['Original'].iloc[i] +'([.,\s]|$)', ' ' + mapOfWords['Map'].iloc[i] + ' ',text, flags=re.IGNORECASE)
    text = text.strip() # Trim string
        
    return text

def clean_txt_stopwords(text):
    
#    removing all punctuations
    remove = string.punctuation
#    remove = remove.replace(".", "") # don't remove dots #in case don't want to remove
    
    text = "".join(l for l in text if l not in remove)
    text = re.sub(' +',' ',text)

#    removing all numbers
    text = re.sub(r'\d+', '',text)
    
    stop=stopWords['StopWords'].tolist()
    text=" ".join(w for w in text.lower().split() if w not in stop)

    return text


# Some extra steps for normalization and removing unnecessary spaces and some improvements of observed issues

#nlp = English() # required both for sentence tokenization and lemmatization
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
#    remove = remove.replace("\'", "") # don't remove '
#    remove = remove.replace("-", "") # don't remove -
    text = "".join(l for l in text if l not in remove)
    text = re.sub(' +',' ',text)
    text = clean_text(text)
    text = re.sub(' +',' ',text)
    text = text.strip()

    return (text.lower())


con = pyodbc.connect('DRIVER={SQL Server};Server=KACH_SAW;Database=WORKAREA;Trusted_Connection=yes;')
cur = con.cursor()
inputSQL="SELECT ID AS RowID,subject_en+' '+Description_Cleaned_En_StopPhrases AS Responses FROM [MST].[t_sample] where AMEX IS NOT NULL"
cur.execute(inputSQL)
rows = cur.fetchall()

commit_batch=0
batch=0
for row in rows:    
    norm=calling_clean_text(row.Responses)
    norm_stopwords=clean_txt_stopwords(calling_clean_text(row.Responses))
#    print(row.RowID)
#    print(norm)
#    print("~~~~~~~~~~~")
#    print(norm_stopwords)
#    print("---------------------------------------------------------")
    cur.execute("UPDATE [MST].[t_Sample] SET DESCRIPTION_NORMALIZED=?, DESCRIPTION_NORMALIZED_STOPWORDS=? WHERE ID=?",(norm,norm_stopwords,row.RowID))
    commit_batch+=1
    if commit_batch % 1000==0:
        con.commit()
        commit_batch=0
        batch+=1
        print(batch)

con.commit()
cur.close()
con.close()
