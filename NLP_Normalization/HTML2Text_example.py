#run directly in python 3.6 (install html2text via pip)

import pyodbc
import html2text
from datetime import datetime
h=html2text.HTML2Text()
h.ignore_links=True


def close_reopen():
    con=pyodbc.connect('DRIVER={SQL Server};Server=kach-laptop;Database=WORKAREA;Trusted_Connection=yes;')
    cur=con.cursor()
    qry="SELECT top 1000 ID,DESCRIPTION FROM MST.t_Sample WHERE DESCRIPTION IS NOT NULL and DESCRIPTION_CLEANED IS NULL"
    cur.execute(qry)
    rows=cur.fetchall()

    batch=0
    cnt=0
    for row in rows:
        cleansed=h.handle(row.DESCRIPTION)
        cur.execute("UPDATE [MST].[t_Sample] SET DESCRIPTION_CLEANED=? WHERE ID=?",(cleansed,row.ID))
        batch+=1
        if batch%100==0:
            cnt+=1
            con.commit()
            print(cnt," ",datetime.now().time())

    con.commit()    
    con.close()

##for i in range(0,46):
##    print('BATCH:',i)
##    close_reopen()
##    

close_reopen()
    
con.commit()    
con.close()



##output="".join(line.strip() for line in output.splitlines())

##print(output)

##for line in output.splitlines():
##    line=line.strip()
##
##    #to eliminate disclaimer, instructions at the bottom of email
##    #if line=='* * *':
##    #    break
##    print(line)
