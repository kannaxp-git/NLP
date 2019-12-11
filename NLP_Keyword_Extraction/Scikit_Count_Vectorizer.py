# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 14:17:36 2018

@author: kach
"""
import pyodbc
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def get_data_SQL_Pandas(server,db,qry):
    con = pyodbc.connect('DRIVER={SQL Server};Server='+server+';Database='+db+';Trusted_Connection=yes;')
    cur = con.cursor()
    df = pd.read_sql(qry, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
    cur.close()
    con.close()
    return df

if __name__=='__main__':
    
    server='EAISOTOPE25'
    db='Workarea_Kannan'
#    con=pyodbc.connect('DRIVER={SQL Server};Server='+ server +';Database='+ db +';Trusted_Connection=yes;')
#    cur=con.cursor()
#    
    ##qry="SELECT top 5 [ID],[Sentence_Norm] as TextForAnalysis FROM [WORKAREA].[dbo].[v_CPE_PowerBI]"
    #qry="select top 10 [RowID] as ID, [normalizedResponses]as TextForAnalysis  from [CUS].[t1_ProcessingSurveyData_Normalized]"
    ##input_table='[WORKAREA].[dbo].[v_CPE_PowerBI]'
    ##qry="SELECT TextForAnalysis from %s"%(input_table)
    
    qry="""
    select top  10 a.Preprocessed_Responses TextForAnalysis from [CUS].[t_Preprocessed_Responses_NEW] a
    join [CUS].[t_SurveyQuestions_FY18H2GESS_Hierarchy] b
    on a.questionid=b.QuestionID
    where b.experience='Meeting' and a.Preprocessed_responses is not null
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
#    print(type(vocabulary))
    for rw,value in vocabulary.items():
        df_out.loc[Idx]=[rw,value]
        Idx+=1
#        print(rw,value)
        
#    cur.execute(qry)
#    rows=cur.fetchall()
#    
#    #cur.execute("TRUNCATE TABLE [CUS].[t1_ProcessingTextRank]")
#    
#    doc=' '.join(row.TextForAnalysis for row in rows)
##    
##    for row in rows:
##        doc=' '.join(row.TextForAnalysis)
#    r=Rake()
#    r.extract_keywords_from_text(doc)
#    keywords=r.get_ranked_phrases_with_scores()
#    print(keywords)
#    #
#    ##    print(row.ID)
#    #    keywords=' '.join(extract_key_phrases(row.TextForAnalysis))
#    #    summary=extract_sentences(row.TextForAnalysis)
#    #    cur.execute("""INSERT INTO [CUS].[t1_ProcessingTextRank] VALUES(?,?,?)""",(row.ID,keywords,summary))
#    
#    con.commit()
#    con.close()
#    
#    print("Completed!")
#                    
