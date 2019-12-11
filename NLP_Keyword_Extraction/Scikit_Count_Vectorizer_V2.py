# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:17:36 2018

@author: kach
"""
import pyodbc
import sqlalchemy
import urllib
import urllib.parse
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

def get_data_SQL_Pandas(server,db,qry):
    con = pyodbc.connect('DRIVER={SQL Server};Server='+server+';Database='+db+';Trusted_Connection=yes;')
    cur = con.cursor()
    df = pd.read_sql(qry, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
    cur.close()
    con.close()
    return df

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
    
    server='EAISOTOPE25'
    db='Workarea_Kannan'
    criteria="'Supporting'"
    qry="""
    select a.Preprocessed_Responses TextForAnalysis from [CUS].[t_Preprocessed_Responses_NEW] a
    join [CUS].[t_SurveyQuestions_FY18H2GESS_Hierarchy] b
    on a.questionid=b.QuestionID
    where b.experience="""+ criteria +""" and a.Preprocessed_responses is not null
    """
    df_in=get_data_SQL_Pandas(server,db,qry)
    corpus=df_in['TextForAnalysis']
    df_out=pd.DataFrame(columns=['Keyword','Score'])
    Idx=0
#    corpus=["March Surface PROMO FR",
#    "March Surface PROMO FR",
#    "Canada Surface Pro 4 and Surafce Book Promo",
#    "Surface Book Q3 Promo i5 256GB Western Europe",
#    "Surface Poland Q3 Entry SKU Promo",
#    "Surface Poland Q3 Entry SKU Promo",
#    "Surface Promo Poland Q3",
#    "Surface Promo Poland Q3",
#    "Surface EDU Promo Communication",
#    "UK Surface Book, Surface Pro 4 Promo",
#    "Canada Surface Pro 4 and Surafce Book Promo",
#    "Taiwan Surface Commercial Bundle Promo",
#    "US Promo SP4 and Surface Book",
#    ]
#    
    corpus=[x.lower() for x in corpus]
    bow= CountVectorizer()
    matrix=bow.fit_transform(corpus)
    #print(matrix)
    
    #print(bow.get_feature_names())
    #print(bow.vocabulary_)
    vocabulary=bow.vocabulary_
    #print(type(vocabulary))
    for rw,value in vocabulary.items():
        df_out.loc[Idx]=[rw,value]
        Idx+=1
        #print(rw,value)
    
    stopwords=set(stopwords.words('english'))

    #    Removing invalid keyphrases
    df_out=df_out[~df_out.Keyword.isin(stopwords)]
    #print(df_out)
    
    df_out['Experience']=criteria
    
    write_data_SQL(df_out,server,db,'t_New_Keywords_ByExperience','CUS','append')
    

#                    
