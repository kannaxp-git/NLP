import urllib2
import urllib
import sys
import base64
import json
import numpy as np
import pandas as pd

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None):

    # Execution logic goes here
    account_key ="30dfaa5b062d4cfdbcfb5547c1467206"#str(dataframe2['Col1'][0])

    base_url = 'https://westus.api.cognitive.microsoft.com/'
   
    headers = {'Content-Type':'application/json', 'Ocp-Apim-Subscription-Key':account_key}

    sentiment_scores = []
    num_examples = len(dataframe1.index)
    input_texts = '{"documents":['

    #for each record
    #dataframe1, dfremain = dataframe1[:10, :], dataframe1[10:, :] if len(dataframe1) > 10 else dataframe1, None
    for i in range(0, num_examples):
        input_text = str(dataframe1['Text'][i])
        input_text = input_text.replace("\"", "'")
            input_texts = input_texts + '{"id":"' + str(i) + '","text":"'+ input_text + '"},'        

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

        df1.append(pd.DataFrame({'SentimentScore':sentiment_scores}))
        dataframe1=dfremain
      
    # Return value must be of a sequence of pandas.DataFrame
    return df1

