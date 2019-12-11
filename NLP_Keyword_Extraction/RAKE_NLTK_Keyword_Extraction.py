# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 03:38:31 2018
Ref: https://github.com/csurfer/rake-nltk
@author: kach
"""
import pyodbc
from rake_nltk import Rake

if __name__=='__main__':
    
    server='EAISOTOPE25'
    db='Workarea_Kannan'
    con=pyodbc.connect('DRIVER={SQL Server};Server='+ server +';Database='+ db +';Trusted_Connection=yes;')
    cur=con.cursor()
    
    ##qry="SELECT top 5 [ID],[Sentence_Norm] as TextForAnalysis FROM [WORKAREA].[dbo].[v_CPE_PowerBI]"
    #qry="select top 10 [RowID] as ID, [normalizedResponses]as TextForAnalysis  from [CUS].[t1_ProcessingSurveyData_Normalized]"
    ##input_table='[WORKAREA].[dbo].[v_CPE_PowerBI]'
    ##qry="SELECT TextForAnalysis from %s"%(input_table)
    
    qry="""
    select b.EXPERIENCE,b.QuestionTitle, a.Preprocessed_Responses TextForAnalysis from [CUS].[t_New_Preprocessed_Responses] a
    join [CUS].[t_SurveyQuestions_FY18H2GESS_Hierarchy] b
    on a.questionid=b.QuestionID
    where b.experience='Meeting' and a.Preprocessed_responses is not null
    """
    cur.execute(qry)
    rows=cur.fetchall()
    
    #cur.execute("TRUNCATE TABLE [CUS].[t1_ProcessingTextRank]")
    
    doc=' '.join(row.TextForAnalysis for row in rows)
#    
#    for row in rows:
#        doc=' '.join(row.TextForAnalysis)
    r=Rake()
    r.extract_keywords_from_text(doc)
    keywords=r.get_ranked_phrases_with_scores()
    print(keywords)
    #
    ##    print(row.ID)
    #    keywords=' '.join(extract_key_phrases(row.TextForAnalysis))
    #    summary=extract_sentences(row.TextForAnalysis)
    #    cur.execute("""INSERT INTO [CUS].[t1_ProcessingTextRank] VALUES(?,?,?)""",(row.ID,keywords,summary))
    
    con.commit()
    con.close()
    
    print("Completed!")
                    
