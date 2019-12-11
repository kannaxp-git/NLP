#https://medium.com/@aneesha/topic-modeling-with-scikit-learn-e80d33668730
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
#from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pyodbc

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        #print("Topic %d:" % (topic_idx))
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))
        
#dataset = fetch_20newsgroups(shuffle=True, random_state=1, remove=('headers', 'footers', 'quotes'))
#documents = dataset.data


con=pyodbc.connect('DRIVER={SQL Server};Server=KACH-LAPTOP;Database=WORKAREA;Trusted_Connection=yes;')
cur=con.cursor()

txtoutput=open("C:\\Users\\kach\\Desktop\\Temp\\topicop.txt","a")
source=('GESS','SNOW')
experience=('ACCESSING','COLLABORATING','COMMUNICATING','FINDING','MEETING','SUPPORTING')

no_features = 1000000
no_topics = 30
no_top_words = 6

for s in source:
    for e in experience:
        print(s,e)
        qry="SELECT NormalizedResponse AS TextForAnalysis from [WORKAREA].[CUS].[t_GESSSNOW_Normalized_Master] where Source='"+s+"' and "+e+">0.3"
        cur.execute(qry)
        rows=cur.fetchall()
        mydata=[row[0] for row in rows]
        documents=mydata

# NMF is able to use tf-idf
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
        tfidf = tfidf_vectorizer.fit_transform(documents)
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
        tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
        tf = tf_vectorizer.fit_transform(documents)
        tf_feature_names = tf_vectorizer.get_feature_names()

# Run NMF
        nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)

# Run LDA
        lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

#        display_topics(nmf, tfidf_feature_names, no_top_words)
#        display_topics(lda, tf_feature_names, no_top_words)
        
        for topic_idx, topic in enumerate(nmf.components_):
            topic=" ".join([tfidf_feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
            outputstring=''.join([s,"\t",e,"\t","NMF","\t",str(no_topics-topic_idx),"\t",topic,"\n"])
            txtoutput.write(outputstring)
        
        for topic_idx, topic in enumerate(lda.components_):
            topic=" ".join([tf_feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])
            outputstring=''.join([s,"\t",e,"\t","LDA","\t",str(no_topics-topic_idx),"\t",topic,"\n"])
            txtoutput.write(outputstring)

txtoutput.close()
con.close()
print('completed!')
