from __future__ import absolute_import
from __future__ import print_function
import six
__author__ = 'a_medelyan'

import rake
import operator
import io
import pyodbc

print("Running...")

con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()

###Drop & Recreate output table
#qry="IF OBJECT_ID('CUS.t_RAKE_Output','U') IS NOT NULL DROP TABLE CUS.t_RAKE_Output;"
#cur.execute(qry)
#qry="CREATE TABLE CUS.t_RAKE_Output (KeyPhrase nvarchar(MAX), Score float)"
#cur.execute(qry)

#for i in range(0,3):
#qry="SELECT Sentence_Norm from %s where survey= '%s' AND SentimentLabel='%s'"%(input_table,survey,sentiment[i])
#qry="SELECT TextForAnalysis from [CUS].[t_RAKE_Input]"
txtoutput=open("C:\\Users\\kach\\Desktop\\Temp\\rakeop.txt","a")
source=('GESS','SNOW')
experience=('ACCESSING','COLLABORATING','COMMUNICATING','FINDING','MEETING','SUPPORTING')
for s in source:
    for e in experience:
        print(s,e)
        qry="SELECT NormalizedResponse AS TextForAnalysis from [WORKAREA].[CUS].[t_GESSSNOW_Normalized_Master] where Source='"+s+"' and "+e+">0.3"
        cur.execute(qry)
        rows=cur.fetchall()
        txt=open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt","w")
        for row in rows:
            row=''.join(map(str,row))
            outputstring=''.join([row,"\n"])
            txt.write(outputstring)
        txt.close()
        
        stoppath="SmartStoplist.txt"
        
        rake_object=rake.Rake(stoppath,3,5,2)
        
        sample_file=io.open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt", 'r',encoding="iso-8859-1")
        text=sample_file.read()
        
        keywords=rake_object.run(text)
        for keyword in keywords:
            op=''.join([s,"\t",e,"\t",keyword[0],"\t",str(keyword[1]),"\n"])
            txtoutput.write(op)
        
        txt.close()

txtoutput.close()
con.commit()
con.close()
print("Completed!")
        
        
#        
#    
#qry="SELECT [dbo].[fn_RemoveNonAlphaCharacters]([TextForAnalysis]) [TextForAnalysis]  FROM [WORKAREA].[CUS].[t_RAKE_Input]"
#cur.execute(qry)
#rows=cur.fetchall()
#txt=open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt","w")
#for row in rows:
#    row=''.join(map(str,row))
#    outputstring=''.join([row,"\n"])
#    txt.write(outputstring)
#txt.close()
#
#
## EXAMPLE ONE - SIMPLE
#stoppath = "SmartStoplist.txt"
#
## 1. initialize RAKE by providing a path to a stopwords file
#rake_object = rake.Rake(stoppath, 5, 3, 4)
#
## 2. run on RAKE on a given text
#sample_file = io.open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt", 'r',encoding="iso-8859-1")
#text = sample_file.read()
#
#keywords = rake_object.run(text)
#
#for keyword in keywords:
#    cur.execute("""INSERT INTO CUS.t_RAKE_Output VALUES(?,?)""",(keyword[0],keyword[1]))
#    
#txt.close()
#
#con.commit()
#con.close()
#
#print("Completed!")
