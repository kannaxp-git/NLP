#run directly in python 3.6 (install html2text via pip)

import pyodbc
import html2text
h=html2text.HTML2Text()
h.ignore_links=True


con=pyodbc.connect('DRIVER={SQL Server};Server=kach_saw;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()

qry="SELECT [INDEX] ID,DESCRIPTION TEXT FROM [dbo].[MST2017ALL] WHERE DESCRIPTION IS NOT NULL and description_cleaned is null "#DESCRIPTION IS NOT NULL AND DESCRIPTION_CLEANED like '%>>%'" #IS NULL"
cur.execute(qry)
rows=cur.fetchall()


cnt=0
for row in rows:
    cleansed=h.handle(row.TEXT)
#    print(row.ID)
#    print(cleansed)
#    print('------------------------------------------------------------------------------------')
    cur.execute("UPDATE [dbo].[MST2017ALL] SET DESCRIPTION_CLEANED=? WHERE [INDEX]=?",(cleansed,row.ID))
    cnt+=1
    if cnt%100==0:
        print(cnt)
        con.commit()
        cnt=0
    
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
