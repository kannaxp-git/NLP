# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 18:10:43 2018

@author: kach
"""

import wordninja
import pandas as pd
import pyodbc
from nltk import word_tokenize

con=pyodbc.connect('DRIVER={SQL Server};Server=localhost;Database=WORKAREA_kannan;Trusted_Connection=yes;')
cur=con.cursor()

qry="SELECT ID, lower([Work Activity Name]) TextForAnalysis from [XLB].[t_OneMap_Sample] where [Work Activity Name] is not null" 
cur.execute(qry)
rows=cur.fetchall()

outputdata=pd.DataFrame(columns=['ID','Text_Normalized'])

indx=0
for row in rows:
    split_str=''
    split_word=''
    tokens= word_tokenize(row.TextForAnalysis)
    for token in tokens:
        split_word= ' '.join(w for w in wordninja.split(token))
        if len(split_word)==(len(token)*2)-1:
            split_word=token
            
        split_str=split_str + split_word + ' '
        
    outputdata.loc[indx]=(row.ID, split_str)
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