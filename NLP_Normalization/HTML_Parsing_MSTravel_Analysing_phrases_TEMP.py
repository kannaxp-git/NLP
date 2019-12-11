# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
import string
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []
    
#    def handle_starttag(self, tag, attrs):
#        print("Encountered a start tag:", tag)
#
#    def handle_endtag(self, tag):
#        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if len(data.strip())>2:# and re.match(r'<[^>]+>',data):
            if re.search("{",data):
                return
            else:
                self.data.append(data)
#            print("Encountered some data  :", data)
        



def clean_text(text):
    w=text
    w = "".join(l for l in w if l not in remove)
    w = re.sub(' +',' ',w)
    w = w.lower().strip()
    
    return w

#DB connection & get data from SQL
import pyodbc 
import pandas

# Read stop words
con = pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur = con.cursor()
stopwordInputSQL="select phrase from [MST].[t_Stop_Phrases]"
stopphrases = pandas.read_sql(stopwordInputSQL, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None)
cur.close()
con.close()



con=pyodbc.connect('DRIVER={SQL Server};Server=kach-laptop;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()
#con.commit()    
#con.close()

qry="SELECT ID,DESCRIPTION FROM MST.t_Sample WHERE ISVALID=1 AND IsEnglish=1 AND DESCRIPTION IS NOT NULL"
cur.execute(qry)
rows=cur.fetchall()

remove = string.punctuation

#batching to overcome SQL memory overflow issue
for row in rows:
    cleansed=''
    parser = MyHTMLParser()
    parser.feed(row.DESCRIPTION)
    stopx=stopphrases['phrase'].tolist()
    cleansed=" ".join(phrase for phrase in parser.data if clean_text(phrase) not in stopx)    
    cur.execute("UPDATE [MST].[t_Sample] SET DESCRIPTION_CLEANEDX=? WHERE ID=?",(cleansed,row.ID))
    con.commit()


#    for phrase in parser.data:
#        w=phrase
#        w = "".join(l for l in w if l not in remove)
#        w = re.sub(' +',' ',w)
#        w = w.lower().strip()
#        cur.execute("INSERT INTO [MST].[t_HTML_Phrases_TBD] values(?,?)",(row.ID,w))
        
        
con.commit()    
con.close()
