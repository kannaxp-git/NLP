#Import library essentials
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in
import pyodbc

#con=pyodbc.connect('DRIVER={SQL Server};azwucsmlprdsql2;Database=WORKAREA_MACHINELEARNING;Trusted_Connection=yes;')
con=pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};Server=tcp:azwucsmlprdsql2,1433;Database=WORKAREA_MACHINELEARNING;Trusted_Connection=yes;')
cur=con.cursor()

qry="select distinct questionidx from [CUS].[t1_ProcessingSurveyData_Normalized] order by questionidx"
cur.execute(qry)
questions=cur.fetchall()
for q in questions:
    print(q.questionidx)
    qry="select NormalizedResponses from [CUS].[t1_ProcessingSurveyData_Normalized] where isvalid=1 and NormalizedResponses=cast(normalizedresponses as varchar)  and questionidx='%s'"%(q.questionidx)
    print(qry)
    cur.execute(qry)
    rows=cur.fetchall()
    txt=open("C:\\Users\\kach\\OneDrive\\iWorks\\Python\\Text Summarization\\SQL2TXT.txt","w", encoding="utf-8" )
    for row in rows:
        row=''.join(map(str,row))
        outputstring=''.join([row,"\n"])
        txt.write(outputstring)
    txt.close()

    file=open("C:\\Users\\kach\\OneDrive\\iWorks\\Python\\Text Summarization\\SQL2TXT.txt",encoding="utf-8")
    parser = PlaintextParser.from_file("C:\\Users\\kach\\OneDrive\\iWorks\\Python\\Text Summarization\\SQL2TXT.txt", Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, 5) #Summarize the document with 5 sentences

    sumx=""
    for sentence in summary:
        sumx=sumx+str(sentence)+"\n"
    cur.execute("""INSERT INTO [dbo].[CPE_TextSumy] VALUES(?,?)""",(q.questionidx,sumx))

con.commit()
con.close()

print("Completed!")


#Q2)How can Microsoft better show you that they 'care about your needs'? 
