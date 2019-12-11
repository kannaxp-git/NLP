#https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words

from math import log
from nltk import word_tokenize
import pyodbc
import re

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
words = open("word-by-frequency.txt").read().split()
#words = open("C:\\Users\\kach\\Desktop\\Temp\\bagofwords.txt").read().split()
wordcost = dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
maxword = max(len(x) for x in words)

def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i-maxword):i]))
        return min((c + wordcost.get(s[i-k-1:i], 9e999), k+1) for k,c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1,len(s)+1):
        c,k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i>0:
        c,k = best_match(i)
        assert c == cost[i]
        out.append(s[i-k:i])
        i -= k

    return " ".join(reversed(out))


#DB connection & get data from SQL
con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
#con=pyodbc.connect('DRIVER={SQL Server};Server=dubcpdmsql08;Database=workarea_machinelearing;Trusted_Connection=yes;')
cur=con.cursor()
qry=" select uniquesentenceid as ID, TextForAnalysis from [CUS].[t_GESSSNOW_Normalized] where isvalid=1"
cur.execute(qry)
rows=cur.fetchall()

txt=open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT_KeywordClean.txt","w")

for row in rows:
    sentence= row.TextForAnalysis #sentence = 'errorresolution sharepoint workaround rw'
    sentence=sentence.replace("\t"," ")
    match=re.findall(r'\d+',sentence) #regular expression to find all concatenated string & number e.g office365 7area
    for m in match:
        sentence=sentence.replace(str(m),' '+str(m)+' ')
    
    sentence =sentence.rstrip().lstrip()
        
    clean_sentence=''
    for token in word_tokenize(sentence):
        cleantoken=infer_spaces(token)
        clean_sentence=clean_sentence+' '+cleantoken
        outputstring=''.join([str(row.ID),"\t",clean_sentence,"\n"])
    
    #print(outputstring)
    txt.write(outputstring)
        
        
#        Identifying misspelled/wrongly concatenated strings
#        if token!=cleantoken:
#            outputstring=''.join([token,"\t",cleantoken,"\n"])
#            txt.write(outputstring)

txt.close()
con.commit()
con.close()