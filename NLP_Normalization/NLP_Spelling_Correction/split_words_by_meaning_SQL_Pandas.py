#https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words

from math import log
from nltk import word_tokenize
import pyodbc
import re
import pandas as pd

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("word-by-frequency.txt").read().split()
AdditionalWords=['sp4','cdsa','crm','fy16','fy17','fy18','365']

print(len(words))

for w in AdditionalWords:
    words.insert(0,w)

print(len(words))

wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))


#DB connection & get data from SQL
con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA_kannan;Trusted_Connection=yes;')
cur=con.cursor()
qry=" select ID, lower([CUS].[fn_RemoveNonAlphaNumbers]([Work Activity Name],' ')) TextForAnalysis from [XLB].[t_OneMap_Sample] where [Work Activity Name] is not null"
cur.execute(qry)
rows=cur.fetchall()

#txt=open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT_KeywordClean.txt","w")
outputdata=pd.DataFrame(columns=['ID','Text_Normalized'])

indx=0
for row in rows:
    clean_sentence=''
    sentence= row.TextForAnalysis
    
    sentence=sentence.replace("\t"," ")
#    match=re.findall(r'\d+',sentence) #regular expression to find all concatenated string & number e.g office365 7area
#    for m in match:
#        sentence=sentence.replace(m,' '+m+' ')
#    sentence =sentence.rstrip().lstrip()

    for tkn in word_tokenize(sentence):
        split_token=infer_spaces(tkn)
        if len(split_token)==(len(tkn)*2)-1:
            split_token=tkn
#            print(tkn,'\t',split_token)
        
        clean_sentence=clean_sentence+split_token+' '
        
    outputdata.loc[indx]=(row.ID, clean_sentence)
    indx+=1
con.close()


import sqlalchemy
import urllib
import urllib.parse

engine = sqlalchemy.create_engine(
        'mssql+pyodbc:///?odbc_connect=%s' % (
		        urllib.parse.quote(
			        'DRIVER={SQL Server};SERVER=localhost;'
			        'DATABASE=WORKAREA_Kannan;Trusted_Connection=yes;')))

connection=engine.connect()
# write the DataFrame to a table in the sql database
outputdata.to_sql("t_Split_Word_By_Meaning", engine,if_exists='replace',schema='dbo') #-----
connection.close()
print("Completed")