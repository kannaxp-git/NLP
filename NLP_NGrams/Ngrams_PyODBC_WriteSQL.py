
import pyodbc
from nltk import ngrams
con = pyodbc.connect('DRIVER={SQL Server};Server=kach-laptop;Database=workarea;Trusted_Connection=yes;')
#con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur = con.cursor()
##cur.execute('SELECT [uniqueSentenceID] as ID,[CUS].[fn_RemoveNonAlphaNumbers]([NormalizedResponses]) as [TEXT] FROM [EnoDataScience].[CUS].[t1_ProcessingSurveyData_Normalized] where NormalizedResponses is not null')
cur.execute('SELECT top 5 [index] ID,[CUS].[fn_RemoveNonAlphaNumbers]([SubjectClean]) [TEXT]  FROM [WORKAREA].[dbo].[MST2017ALL_subjectClean] order by [index]')
rows = cur.fetchall()
cur.execute('TRUNCATE TABLE [MST].[t_Ngram_Output]')
print('Started...')
for row in rows:
    # 1. Split text into sentences
    print(row.ID)
    grams=ngrams(row.TEXT.split(),1)
    for gram in grams:
        gram=''.join(gram)
        cur.execute("INSERT INTO [MST].[t_Ngram_Output] VALUES(?,?)",(row.ID,gram))

print("Removing Stop words")
cur.execute("delete N FROM [WORKAREA].[MST].[t_Ngram_Output] N join [MST].[t_ConfigStopwords] S on N.NGram=S.[StopWords]")

print("Completed!")
con.commit()
con.close()

