from __future__ import absolute_import
from __future__ import print_function
import six
__author__ = 'a_medelyan'

import rake
import operator
import io
import pyodbc
import pandas as pd
import sqlalchemy
import urllib
import urllib.parse
import time

def write_data_SQL(df,server,db,tableName,schemaName='dbo',append_replace='replace'):
    #Sample call: write_data_SQL(hashtags,'localhost','workarea_kannan','t_tablename')
    engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect=%s' % (
            urllib.parse.quote('DRIVER={SQL Server};SERVER='+server+';''DATABASE='+db+
                               ';Trusted_Connection=yes;')))

    connection=engine.connect()
    # write the DataFrame to a table in the sql database
    df.to_sql(tableName, engine,if_exists=append_replace,schema=schemaName)
    connection.close()


if __name__=='__main__':
        
    print("Running...")
    server="EAISOTOPE25"
    db="WORKAREA_KANNAN"
    con=pyodbc.connect('DRIVER={SQL Server};Server='+ server +';Database='+db+';Trusted_Connection=yes;')
    cur=con.cursor()
    
    experience=('ACCESSING','COLLABORATING','COMMUNICATING','FINDING','MEETING','SUPPORTING')

    for e in experience:
        qry="""
        select top 10 b.EXPERIENCE,b.QuestionTitle, a.Preprocessed_Responses TextForAnalysis from [CUS].[t_New_Preprocessed_Responses] a
        join [CUS].[t_SurveyQuestions_FY18H2GESS_Hierarchy] b
        on a.questionid=b.QuestionID
        where b.experience='"""+ e +"""' and a.Preprocessed_responses is not null
        """
        cur.execute(qry)
        rows=cur.fetchall()
        txt=open("SQL2TXT.txt","w")
        for row in rows:
            row=''.join(map(str,row))
            outputstring=''.join([row,"\n"])
            txt.write(outputstring)
        txt.close()
        
        stoppath="SmartStoplist.txt"
        
        rake_object=rake.Rake(stoppath,3,5,2)
        
        sample_file=io.open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt", 'r',encoding="iso-8859-1")
        text=sample_file.read()
        
        idx=0
        keywords=rake_object.run(text)
        
        df_out=pd.DataFrame(keywords,columns=['Score','Keyphrase'])
#        for keyword in keywords:
#            df_out.loc(idx)=[e,keyword[0],keyword[1]]
#            idx+=1
#            
    con.commit()
    con.close()
    print("Completed!")
    