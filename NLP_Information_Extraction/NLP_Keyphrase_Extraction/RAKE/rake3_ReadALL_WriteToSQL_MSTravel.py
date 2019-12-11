from __future__ import absolute_import
from __future__ import print_function

import rake
import io
import pyodbc

print("Running...")

con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()

##Drop & Recreate output table
qry="IF OBJECT_ID('MST.t_RAKE_Output','U') IS NOT NULL DROP TABLE CUS.t_RAKE_Output;"
cur.execute(qry)
qry="CREATE TABLE MST.t_RAKE_Output (KeyPhrase nvarchar(MAX), Score float)"
cur.execute(qry)

#for i in range(0,3):
#qry="SELECT Sentence_Norm from %s where survey= '%s' AND SentimentLabel='%s'"%(input_table,survey,sentiment[i])
#qry="SELECT TextForAnalysis from [CUS].[t_RAKE_Input]"
#qry="SELECT [dbo].[fn_RemoveNonAlphaCharacters]([TextForAnalysis]) [TextForAnalysis]  FROM [WORKAREA].[CUS].[t_RAKE_Input]"
qry="SELECT Description_Normalized_StopWords as [TextForAnalysis]  FROM [WORKAREA].MST.t_Sample where Description_Normalized is not null"
cur.execute(qry)
rows=cur.fetchall()
txt=open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt","w")
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
sample_file = io.open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt", 'r',encoding="iso-8859-1")
text = sample_file.read()

keywords = rake_object.run(text)

for keyword in keywords:
    cur.execute("""INSERT INTO MST.t_RAKE_Output VALUES(?,?)""",(keyword[0],keyword[1]))
    
txt.close()

con.commit()
con.close()

print("Completed!")
