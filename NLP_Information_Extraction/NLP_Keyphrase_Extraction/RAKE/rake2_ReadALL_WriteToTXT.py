from __future__ import absolute_import
from __future__ import print_function
import six
__author__ = 'a_medelyan'

import rake
import operator
import io
import pyodbc


##InpTable="dbo.t_PyInput"        #Notes Input Table
##PrcTable="dbo.t_RAKE_Output"   #Processing Table

con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()

##qry="IF OBJECT_ID('CPE.t_RAKE_Output','U') IS NOT NULL DROP TABLE CPE.t_RAKE_Output;"
##cur.execute(qry)
##qry="CREATE TABLE CPE.t_RAKE_Output (Phrase nvarchar(255), Score float)"
##cur.execute(qry)
cur.execute("select Sentence_Norm from [WORKAREA].[CPE].[t_Sentence_Tokenized4] where survey ='H2FY16_SMSP_Managed'")
rows=cur.fetchall()
txt=open("C:\\Users\\kach\\Documents\\My_Stuff\\iWORKS\\My_Python\\RAKE\\RAKE\\SQL2TXT.txt","w")
for row in rows:
    row=''.join(map(str,row))
    outputstring=''.join([row,"\n"])
    txt.write(outputstring)
txt.close()
#con.close()


# EXAMPLE ONE - SIMPLE
stoppath = "SmartStoplist.txt"

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath, 5, 3, 4)

# 2. run on RAKE on a given text
sample_file = io.open("C:\\Users\\kach\\Documents\\My_Stuff\\iWORKS\\My_Python\\RAKE\\RAKE\\SQL2TXT.txt", 'r',encoding="iso-8859-1")
text = sample_file.read()

keywords = rake_object.run(text)
txt=open("C:\\Users\\kach\\Documents\\My_Stuff\\iWORKS\\My_Python\\RAKE\\RAKE\\H2CPE_RAKE_Output.txt","w")
i=1
for keyword in keywords:
    txt.write(''.join([str(i),",",keyword[0],",",str(keyword[1]),"\n"]))
    print(i,keyword[0],",",keyword[1])
    i=i+1
    #cur.execute("""INSERT INTO CPE.t_RAKE_Output VALUES(?,?)""",(keyword[0],keyword[1]))
txt.close()
con.close()

# 3. print results
#print("Keywords:", keywords)

print("----------")
### EXAMPLE TWO - BEHIND THE SCENES (from https://github.com/aneesha/RAKE/rake.py)
##
### 1. initialize RAKE by providing a path to a stopwords file
##rake_object = rake.Rake(stoppath)
##
##text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility " \
##       "of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. " \
##       "Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating"\
##       " sets of solutions for all types of systems are given. These criteria and the corresponding algorithms " \
##       "for constructing a minimal supporting set of solutions can be used in solving all the considered types of " \
##       "systems and systems of mixed types."
##
##
##
### 1. Split text into sentences
##sentenceList = rake.split_sentences(text)
##
##for sentence in sentenceList:
##    print("Sentence:", sentence)
##
### generate candidate keywords
##stopwordpattern = rake.build_stop_word_regex(stoppath)
##phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern)
##print("Phrases:", phraseList)
##
### calculate individual word scores
##wordscores = rake.calculate_word_scores(phraseList)
##
### generate candidate keyword scores
##keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
##for candidate in keywordcandidates.keys():
##    print("Candidate: ", candidate, ", score: ", keywordcandidates.get(candidate))
##
### sort candidates by score to determine top-scoring keywords
##sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
##totalKeywords = len(sortedKeywords)
##
### for example, you could just take the top third as the final keywords
##for keyword in sortedKeywords[0:int(totalKeywords / 3)]:
##    print("Keyword: ", keyword[0], ", score: ", keyword[1])
##
##### EXAMPLE THREE - Directly calling RAKE
####print(rake_object.run(text))
