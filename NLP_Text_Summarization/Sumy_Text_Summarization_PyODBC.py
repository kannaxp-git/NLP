#Import library essentials
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in
import pyodbc
import io
import operator

con=pyodbc.connect('DRIVER={SQL Server};Server=DUBCPDMSQL08;Database=WORKAREA_MACHINELEARNING;Trusted_Connection=yes;')
cur=con.cursor()

qry="select distinct VerbatimQuestionID from [CPE].[t_Sentence_Tokenized4_H2FY16SMSPManaged1]order by VerbatimQuestionID"
cur.execute(qry)
questions=cur.fetchall()
for q in questions:
    print(q.VerbatimQuestionID)
    qry="select sentence_norm from [CPE].[t_Sentence_Tokenized4_H2FY16SMSPManaged1] where verbatimQuestionID=%s"%(q.VerbatimQuestionID)
    cur.execute(qry)
    rows=cur.fetchall()
    txt=open("C:\\Users\\kach\\OneDrive\\iWorks\\Python\\Text Summarization\\SQL2TXT.txt","w")
    for row in rows:
        row=''.join(map(str,row))
        outputstring=''.join([row,"\n"])
        txt.write(outputstring)
    txt.close()

    file="C:\\Users\\kach\\OneDrive\\iWorks\\Python\\Text Summarization\\SQL2TXT.txt"
    parser = PlaintextParser.from_file(file, Tokenizer("english"))
    summarizer = LexRankSummarizer()

    summary = summarizer(parser.document, 5) #Summarize the document with 5 sentences

    sumx=""
    for sentence in summary:
        sumx=sumx+str(sentence)+"\n"
    cur.execute("""INSERT INTO [CPE].[t_Sentence_Tokenized4_H2FY16SMSPManaged1_TxtSummary] VALUES(?,?)""",(q.VerbatimQuestionID,sumx))

con.commit()
con.close()

print("Completed!")


#Q2)How can Microsoft better show you that they 'care about your needs'? 
