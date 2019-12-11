import urllib2
import urllib
import sys
import base64
import json
import numpy as np
import pandas as pd

import io
import operator
import pyodbc

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1):

    # Execution logic goes here
    account_key ="30dfaa5b062d4cfdbcfb5547c1467206"#str(dataframe2['Col1'][0])

    base_url = 'https://westus.api.cognitive.microsoft.com/'
   
    headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}
    df1=pd.DataFrame()

    for r in range(1,84):
        if len(dataframe1)>3:
            dfremain=dataframe1[3:]
            dataframe1=dataframe1[:3]

        sentiment_scores = []
        num_examples = len(dataframe1.index)
        input_texts = '{"documents":['

        #for each record
        for i in range(0, num_examples):
            input_text= dataframe1['Text'][i].encode('utf-8')
            #input_text = str(dataframe1['Text'][i])
            input_text = input_text.replace("\"", "'")
            #input_texts = input_texts + '{"id":"' + str(i) + '","text":"'+ input_text + '"},'
            input_texts = input_texts + '{"id":"' + str(dataframe1['id'][i]) + '","text":"'+ input_text + '"},'        

        input_texts = input_texts + ']}'
        #print input_texts
        
        # Detect sentiment.
        batch_sentiment_url = base_url + 'text/analytics/v2.0/sentiment'        
                           
        req = urllib2.Request(batch_sentiment_url, input_texts, headers) 
        response = urllib2.urlopen(req)
        result = response.read()
        obj = json.loads(result)
           
        for sentiment_analysis in obj['documents']:            
            sentiment_scores.append( str(sentiment_analysis['score']))  

        sentiment_scores = pd.Series(np.array(sentiment_scores))        

        #if df1 is None:
        #    df1 = pd.DataFrame({'id':dataframe1['id'],'SentimentScore':sentiment_scores})

        #if df1 is not None:
        df1=df1.append(pd.DataFrame({'id':dataframe1['id'],'SentimentScore':sentiment_scores}))

##        print(df1)
##        print('\n')
        dataframe1=dfremain
        dataframe1 = dataframe1.reset_index(drop=True)
          
    # Return value must be of a sequence of pandas.DataFrame
    return df1


#main--------------------------
#http://stackoverflow.com/questions/12047193/how-to-convert-sql-query-result-to-pandas-data-structure
con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
#cur=con.cursor()
sql='select id ,EnglishComment as Text from [CPE].[t_CPE_Consolidated_View1] where EnglishComment is not null'
#cur.execute(sql)
#rows=cur.fetchall()
#print(cur.keys())

df_in=pd.read_sql(sql,con)
df_out=azureml_main(df_in)

#txt=open("C:\\Users\\kach\\Documents\\My_Stuff\MSWorks\\Sentiment_Analysis\\CPE_France\\TextAPI_Output.txt","a")
#txt.write(azureml_main(df))

df_out.to_csv(r'C:\\Users\\kach\\Documents\\My_Stuff\MSWorks\\Sentiment_Analysis\\CPE_France\\TextAPI_Output.txt', header=None, index=None, sep=',', mode='a')
print('Completed!')
con.close()
