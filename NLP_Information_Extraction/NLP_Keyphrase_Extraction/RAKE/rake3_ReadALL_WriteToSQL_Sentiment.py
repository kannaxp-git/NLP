from __future__ import absolute_import
from __future__ import print_function
import six
__author__ = 'a_medelyan'

import rake
import operator
import io
import pyodbc


con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()

input_table='[WORKAREA].[dbo].[v_CPE_PowerBI]'
survey='H2FY16 SMSP Unmanaged'
sentiment=["Positive","Negative","Neutral"]


##Drop & Recreate output table
##qry="IF OBJECT_ID('CPE.t_RAKE_LoopOutput','U') IS NOT NULL DROP TABLE CPE.t_RAKE_LoopOutput;"
##cur.execute(qry)
##qry="CREATE TABLE CPE.t_RAKE_LoopOutput (Survey nvarchar(255), Sentiment nvarchar(50),KeyPhrase nvarchar(255), Score float)"
##cur.execute(qry)

for i in range(0,3):
    qry="SELECT Sentence_Norm from %s where survey= '%s' AND SentimentLabel='%s'"%(input_table,survey,sentiment[i])
    cur.execute(qry)
    rows=cur.fetchall()
    txt=open("C:\\Users\\kach\\Documents\\My_Stuff\\iWORKS\\My_Python\\RAKE\\RAKE\\SQL2TXT.txt","w")
    for row in rows:
        row=''.join(map(str,row))
        outputstring=''.join([row,"\n"])
        txt.write(outputstring)
    txt.close()


    # EXAMPLE ONE - SIMPLE
    stoppath = "SmartStoplist.txt"

    # 1. initialize RAKE by providing a path to a stopwords file
    rake_object = rake.Rake(stoppath, 5, 3, 4)

    # 2. run on RAKE on a given text
    sample_file = io.open("C:\\Users\\kach\\Documents\\My_Stuff\\iWORKS\\My_Python\\RAKE\\RAKE\\SQL2TXT.txt", 'r',encoding="iso-8859-1")
    text = sample_file.read()

    keywords = rake_object.run(text)

    for keyword in keywords:
        cur.execute("""INSERT INTO CPE.t_RAKE_LoopOutput VALUES(?,?,?,?)""",(survey,sentiment[i],keyword[0],keyword[1]))
        
    txt.close()

con.commit()
con.close()

print("Completed!")
