#https://nicschrading.com/project/Intro-to-NLP-with-spaCy/
#https://github.com/NSchrading/intro-spacy-nlp

from spacy.en import English
from subject_object_extraction import findSVOs
from subject_object_extraction import findSVs
from subject_object_extraction_TRY import findSVOs2
import pyodbc
import numpy as np

#DB connection & get data from SQL
con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()
qry="select Number,TextForAnalysis from CUS.t_Spacy_SVOextraction_Input"
cur.execute(qry)
rows=cur.fetchall()

##Initializing Parser
parser=English()
for row in rows:
    i=0
    inpSentence = row.TextForAnalysis
    parsedData=parser(inpSentence)

    for sent in parsedData.sents:
        i=i+1
        svos=findSVOs2(sent)
        str1 = ' '.join(str(e) for e in sent)
        str2=""
        for svo in svos:
            if np.size(svo)>1:
                for token in svo:
                    str2=str2 +" "+ token
            else:
                str2=str2 +" "+ svo
            str2=str2+", "

        cur.execute("""INSERT INTO CUS.t_Spacy_SVOextraction_Output(number,SentenceID,Sentence,SVOs) VALUES(?,?,?,?)""",(row.Number,i,str1,str2))

print("Completed!")
con.commit()
con.close()
##
##parser=English()
##inpSentence="And please tell us what is the difference .    Manager Name : Chung - Wei Foong   Manager Alias : chungwf    Business Justification : It 's blocking SCCM testing .    "
##parsedData=parser(inpSentence)
##for sent in parsedData.sents:
##    svos=findSVOs2(sent)
##    #str1 = ' '.join(str(e) for e in sent)
##    str2=""
##    for svo in svos:
##        if np.size(svo)>1:
##            for token in svo:
##                str2=str2 +" "+ token
##        else:
##            str2=str2 +" "+ svo
##            
##        str2=str2+", "
##
##    print(str2)
##    

####    print(findSVOs(sent))
##    
##
####
####for span in parsedData.sents:
####    sent = [parsedData[i] for i in range(span.start, span.end)]
####    print(findSVOs(sent))
######    break
##
##
####
####
####
####sents=[]
####for span in parsedData.sents:
####    sent=''.join(parsedData[i].string for i in range(span.start,span.end)).strip()
####    sents.append(sent)
####
####for sentence in sents:
####    print(findSVOs(parser(sentence)))
##
##
### can still work even without punctuation
###parse = parser("he and his brother shot me and my sister")
##parse = parser("We are doing failback and having issues")
##print(findSVOs(parse))
##
##parse = parser("We are doing failback and having issues")
##print(findSVOs2(parse))


