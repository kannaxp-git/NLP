from __future__ import absolute_import
from __future__ import print_function
import six
__author__ = 'a_medelyan'

import rake
import operator
import io
import pyodbc

con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()
cur.execute('select UniqueID as ID,Sentence as [TEXT] from CPE.t_Sentence_Tokenized2')
rows=cur.fetchall()
### EXAMPLE ONE - SIMPLE
stoppath = "SmartStoplist.txt"
# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath)
txt=open("C:\\Users\\kach\\Documents\\My_Stuff\\MSWorks\\Sentiment_Analysis\\ConnectedUserSentiment\\RAKE_Output_CPE2.txt","w")
for row in rows:
    # 1. Split text into sentences
    keywords=rake_object.run(row.TEXT)
    for keyword in keywords:
        print([str(row.ID),",",keyword[0],",",str(keyword[1]),"\n"])
        txt.write(''.join([str(row.ID),",",keyword[0],",",str(keyword[1]),"\n"]))
txt.close()
con.close()



##
### 1. initialize RAKE by providing a path to a stopwords file
##rake_object = rake.Rake(stoppath, 5, 3, 4)
##
### 2. run on RAKE on a given text
##sample_file = io.open("C:\\Users\\kach\\Documents\\My_Stuff\\iWORKS\\My_Python\\RAKE\\RAKE\\SQL2TXT.txt", 'r',encoding="iso-8859-1")
##text = sample_file.read()
##
##keywords = rake_object.run(text)
##txt=open("C:\\Users\\kach\\Documents\\My_Stuff\\iWORKS\\My_Python\\RAKE\\RAKE\\RAKE_Output.txt","w")
##for keyword in keywords:
##    txt.write(''.join([keyword[0],",",str(keyword[1]),"\n"]))
##    #print(keyword[0],",",keyword[1])
##    #cur.execute("""INSERT INTO CPE.t_RAKE_Output VALUES(?,?)""",(keyword[0],keyword[1]))
##txt.close()
##con.close()
##
### 3. print results
###print("Keywords:", keywords)
##
##print("----------")
### EXAMPLE TWO - BEHIND THE SCENES (from https://github.com/aneesha/RAKE/rake.py)
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

##### EXAMPLE THREE - Directly calling RAKE
####print(rake_object.run(text))
