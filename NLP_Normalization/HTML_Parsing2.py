# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import re
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
        


#DB connection & get data from SQL
import pyodbc
con=pyodbc.connect('DRIVER={SQL Server};Server=kach-laptop;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()
#con.commit()    
#con.close()

qry="SELECT ID,DESCRIPTION FROM MST.t_Sample WHERE ISVALID=1 AND IsEnglish=1 AND DESCRIPTION IS NOT NULL"
cur.execute(qry)
rows=cur.fetchall()

#batching to overcome SQL memory overflow issue
commit_batch=0
batch=0
for row in rows:
    cleansed=''
    parser = MyHTMLParser()
    parser.feed(row.DESCRIPTION)
    cleansed=' '.join(parser.data)
    
    #for w in parser.data:
    #    print("TOKEN:",w)

    cur.execute("UPDATE [MST].[t_Sample] SET DESCRIPTION_CLEANED=? WHERE ID=?",(cleansed,row.ID))
    commit_batch+=1
    if commit_batch % 1000==0:
        con.commit()
        commit_batch=0
        batch+=1
        print(batch)
        
con.commit()    
con.close()
