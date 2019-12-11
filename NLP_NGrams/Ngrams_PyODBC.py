import pyodbc
from nltk import ngrams

con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()
cur.execute('SELECT ID, cast(description_cleaned as varchar(max)) as [TEXT] FROM [WORKAREA].mst.t_Sample50K where Description_cleaned is not null order by ID')
rows=cur.fetchall()
### EXAMPLE ONE - SIMPLE
#stoppath = "SmartStoplist.txt"
# 1. initialize RAKE by providing a path to a stopwords file
#rake_object = rake.Rake(stoppath)
txt=open("C:\\Users\\kach\\Desktop\\Temp\\NGramsOutput2.txt","w")
N=2
for row in rows:
    print(row.ID)
    # 1. Split text into sentences
    grams=ngrams(row.TEXT.split(),N)
    for gram in grams:
        gram=''.join(gram)
        txt.write(''.join([str(row.ID),",",gram,"\n"]))
txt.close()
con.close()

