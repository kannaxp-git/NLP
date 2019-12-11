import textacy
import textacy.datasets
import pyodbc


cw = textacy.datasets.CapitolWords()
print(type(cw))
cw.download()
records = cw.records(speaker_name={'Hillary Clinton', 'Barack Obama'})

con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()
#qry="SELECT [dbo].[fn_RemoveNonAlphaCharacters]([TextForAnalysis]) text  FROM [WORKAREA].[CUS].[t_RAKE_Input]"
qry="SELECT [TextForAnalysis] text  FROM [WORKAREA].[CUS].[t_RAKE_Input]"
cur.execute(qry)
rows=cur.fetchall()

##txt=open("C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt","w")
##for row in rows:
##    row=''.join(map(str,row))
##    outputstring=''.join([row,"\n"])
##    txt.write(outputstring)
##txt.close()
##
##filepath="C:\\Users\\kach\\Desktop\\Temp\\SQL2TXT.txt"
##records=textacy.fileio.read.read_file(filepath, mode=u'rt', encoding=None)


##text_stream, metadata_stream = textacy.fileio.split_record_fields(records, 'text')
##corpus = textacy.Corpus('en', texts=text_stream, metadatas=metadata_stream)
##
###corpus
##vectorizer=textacy.Vectorizer(weighting='tfidf',normalize=True,smooth_idf=True,min_df=2,max_df=0.95)
##doc_term_matrix=vectorizer.fit_transform(
##    (doc.to_terms_list(ngrams=1,named_entities=True, as_strings=True)
##     for doc in corpus))
##
###print(repr(doc_term_matrix))
##model = textacy.TopicModel('nmf', n_topics=10)
##model.fit(doc_term_matrix)
##doc_topic_matrix = model.transform(doc_term_matrix)
##
###doc_topic_matrix.shape
##for topic_idx, top_terms in model.top_topic_terms(vectorizer.id_to_term, top_n=10):
##    print('topic', topic_idx, ':', '   '.join(top_terms))

con.close()
