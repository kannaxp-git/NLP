"""
Author: Kanna Chandrasekaran
Alias: kach@microsoft.com
Date: 07/16/2018
Description: Python script for Extractive Text-Summarization
"""

#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#from gensim.summarization import summarize
import pyodbc
#from nltk import ngrams
#from nltk.stem import WordNetLemmatizer
#import re
import pandas as pd
import sqlalchemy
import urllib
import urllib.parse
#import io
#import operator


#import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from pycorenlp import StanfordCoreNLP


def get_data_SQL(server,db,qry):
    con = pyodbc.connect('DRIVER={SQL Server};Server='+server+';Database='+db+';Trusted_Connection=yes;')
    cur = con.cursor()
    cur.execute(qry)
    rows = cur.fetchall()
    con.close()
    return rows

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
            urllib.parse.quote('DRIVER={SQL Server};SERVER='+server+';''DATABASE='+db+';Trusted_Connection=yes;')))

    connection=engine.connect()
    # write the DataFrame to a table in the sql database
    df.to_sql(tableName, engine,if_exists=append_replace,schema=schemaName)
    connection.close()


#Calculate Vader Sentiment
def calc_vadersentiment(df_in):
    df_out=pd.DataFrame(columns=['ID','neg','neu','pos','compound'])
    analyzer=SentimentIntensityAnalyzer()
    idx=0
    for index,row in df_in.iterrows():
        vs=analyzer.polarity_scores(row[1])
        df_out.loc[idx]=[row[0],vs['neg'],vs['neu'],vs['pos'],vs['compound']]
        idx+=1
    return df_out


def calc_stanford_corenlp_sentiment(df_in):
    nlp = StanfordCoreNLP('http://localhost:9000')
    df_out=pd.DataFrame(columns=['ID','Idx','Sentence','SentimentValue','Sentiment'])
    
    idx=0
    for index,row in df_in.iterrows():
        print(row[0])
        res = nlp.annotate(row[1],
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 10000,
                   })
        for s in res["sentences"]:
            sentence=" ".join([t["word"] for t in s["tokens"]])
            df_out.loc[idx]=[row[0],s["index"],sentence,s["sentimentValue"], s["sentiment"]]
            idx+=1
    return df_out


if __name__=='__main__':
    idx=0
    server="EAISOTOPE25"
    db="WORKAREA_KANNAN"
    qry="""
    select A.RowID, REPLACE(REPLACE([Responses], CHAR(13), ''), CHAR(10), '') Responses from [CUS].[t1_ProcessingSurveyData] a
    join [CUS].[t_SurveyQuestions_FY18H2GESS_Hierarchy] b
    on a.QuestionId=b.questionid
    where b.[QuestionBusinessType]='Verbatim'
    ---and A.RowID not in (select ID from CUS.t_New_Setiment_StanfordCorenlp )
    """
    df_in=get_data_SQL_Pandas(server,db,qry)
#    -------------VADER--------------------------------
#    df_out=calc_vadersentiment(df_in)
#    write_data_SQL(df_out,server,db,'t_New_Setiment_VaderSentiment','CUS','replace')
#    ---------------------------------------------------
#    -----------STANFORD-CORENLP------------------------
    df_out=calc_stanford_corenlp_sentiment(df_in)
    write_data_SQL(df_out,server,db,'t_New_Setiment_StanfordCorenlp','CUS','replace')
#    ---------------------------------------------------
#   
    print('completed!')
    
#    outputdata=pd.DataFrame(columns=['attribute','value','summaryof','summary'])
#    attribute='[Audiences Impacted (All)]'
    
#    filters=['Partner','Advertiser','Business Customer','Consumer','Developer','Employee','Field','None','Other']
    
#    for q in qrylist:
#        summaryof=q[0]
#        for f in filters:
#            print(q[0])
#            print(f)
#            qry="select "+ q[1] +" [TEXT] FROM [OneMapReporting].[dbo].[Work Activity Details] (NOLOCK) where [Primary GTM] IN ('Partner Led','Field Seller Led') AND [Request Type] <> 'Run Work' and "+ attribute +" like'%" + f + "%'"
#            print(qry)
#            print('--------------------------------------------------------')
#            #rows=get_data_SQL('localhost','workarea_kannan',qry)
#            rows=get_data_SQL('AZ4OBIP1MPSQL01','OneMapReporting',qry)
#            data=""
#            for row in rows:
#                data=''.join([data,row.TEXT,"\n"])
#            
#            if data is not None:
#                summary=summarize(data, word_count=50)
#                outputdata.loc[idx]=[attribute,f,summaryof,summary]
#                idx+=1
#
##    print(outputdata)
#    write_data_SQL(outputdata,'localhost','workarea_kannan','t_summary','XLB','append')
#    print('completed!!!')
#
#
#
#
##   