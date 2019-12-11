#run directly in python 3.6 (install html2text via pip)

import pyodbc
import re

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def isvalid_line(line):
    line=line.strip()

    #minimum length criteria
    if len(line)<=5:
        return 0
    #** email headers #! Links  #- Line breaks  #\ Line breaks (orginal message)
    if left(line,2)=='**' or left(line,1)=='!' or left(line,1)=='-' or left(line,1)=='\\' or left(line,1)=='//':
        return 0
    
    #EMAIL HEADERS
    invalid_prefixes=['EMAIL:','E:','E-MAIL:','FROM:','TO:','CC:','SENT:','SUBJECT:','PHONE:','PH','OFFICE:','MOBILE:','TEL:','TEL','FAX:','DATE:','SENT:**','TO:**','SUBJECT:**','IMPORTANCE:']
    start_token=line.split(' ',1)[0]
    if start_token.upper() in invalid_prefixes:
        return 0
    
    #HTTP addresses
    if left(line,4).upper()=='HTTP':
        return 0

    #single word as a line
    if line.count(' ')<1:
        return 0
    
    return 1

con=pyodbc.connect('DRIVER={SQL Server};Server=kach_saw;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()

qry="SELECT top 50 PERCENT ID,DESCRIPTION_CLEANED_EN TEXT FROM MST.t_SampleDES" 
cur.execute(qry)
rows=cur.fetchall()

batch=1
cnt=0
for row in rows:
    for line in row.TEXT.splitlines():
        line=line.strip()
        if isvalid_line(line): #print(isvalid_line(line),'-',line)
            cur.execute("insert into mst.t_stopphrases select ?",(line))
            cnt+=1
            if cnt%100==0:
                print(batch)
                con.commit()
                cnt=0
                batch+=1
    
con.commit()
con.close()


##        if isvalid_line(line):
##            print('-',line)
##        cur.execute("UPDATE [MST].[t_Sample] SET DESCRIPTION_CLEANED=? WHERE ID=?",(cleansed,row.ID))


##output="".join(line.strip() for line in output.splitlines())

##print(output)

##for line in output.splitlines():
##    line=line.strip()
##
##    #to eliminate disclaimer, instructions at the bottom of email
##    #if line=='* * *':
##    #    break
##    print(line)
