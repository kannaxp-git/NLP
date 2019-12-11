import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import operator
import io
import pyodbc


#
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#sid=SentimentIntensityAnalyzer()
#con=pyodbc.connect('DRIVER={SQL Server};Server=DUBCPDMSQL08.EUROPE.CORP.MICROSOFT.COM;Database=WORKAREA_MACHINELEARNING;Trusted_Connection=yes;')
#con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
#cur=con.cursor()
#sql="select ID, [Text] from [dbo].[t_Sentiment_Input_API1]"
#cur.execute(sql)
#rows=cur.fetchall()
#
#txt=open("C:\\Users\\kach\\Documents\\My_Stuff\MSWorks\\Sentiment_Analysis\\ConnectedUserSentiment\\VaderSentiment_Output_Row.txt","w")
#txt.write("ID,POSITIVE,NEUTRAL,NEGATIVE,COMPOUND \n")
#print("Calculating sentiment...")

analyzer=SentimentIntensityAnalyzer()
vs=analyzer.polarity_scores("This is a horrible internal experience.")
print(vs)



#for row in rows:
#    vs=analyzer.polarity_scores(row.Text)
#    txt.write(''.join([str(row.ID),",",str(vs['pos']),",",str(vs['neu']),",",str(vs['neg']),",",str(vs['compound']),"\n"]))
#print("Job completed.")
#con.close()
#txt.close()
##for s in vs:
##    print(s,vs[s])
##print(vs['pos'],vs['neu'],vs['neg'],vs['compound'])
