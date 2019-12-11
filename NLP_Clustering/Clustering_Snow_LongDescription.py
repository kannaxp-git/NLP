import os
my_path = "C:\\Users\\kach\\Desktop\\Temp\\"
os.chdir(my_path)


# Copy pasting from clustering.py file
import collections
import pandas as pd
import numpy as np
import sklearn
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from scipy.spatial.distance import cdist, pdist
import xlsxwriter
from datetime import datetime
import matplotlib.pylab as pl
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples, silhouette_score
from collections import Counter
from collections import OrderedDict
import re
import string
import operator
import matplotlib.ticker as mticker
import pyodbc

# Setting input values
numberOfWords = 5
numberOfClusters = 20
maxNumberOfClusters = 20
minngrams = 1
maxngrams = 1

# File name to be used
stopwordfiles = 'FY16EPG'
files = 'FY16_EPG'
FileList = ['FY16_EPG'] 

inputFolder = "Input\\"
outputFolder = "Output\\"
fileFolder = "FY16EPG\\"

dbTableName = "t_FY16_EPG"

stopwordfile = stopwordfiles + '_stopwords'

#print(datetime.strftime(datetime.now(), '%H:%M:%S')+" Reading Stop Words File "+ stopwordfile)
#stopwordsfromfile=pd.read_excel(inputFolder + stopwordfile+ ".xlsx", na_values = "NaN", keep_default_na = False)

stopwords_custom = []
##for row in stopwordsfromfile.StopWords:
##    stopwords_custom.append(str(row))


# Append new stopwords from DB
con = pyodbc.connect('DRIVER={SQL Server};Server=dubcpdmsql08;Database=Workarea_MachineLearning;Trusted_Connection=yes;')
#con = pyodbc.connect('DRIVER={SQL Server};Server=kach-laptop;Database=Workarea;Trusted_Connection=yes;')
cur = con.cursor()
cur.execute('SELECT FindWhat FROM [Workarea_MachineLearning].[dbo].[t_Stopwords_Dictionary]')
rows = cur.fetchall()

for row in rows:
    stopwords_custom.append(row.FindWhat)

cur.close()
con.close()

# These words needs to be removed after stemming
special_handling_words={'go', 'get', 'abl', 'seem', 'give', 'make'}

# random_state for kmeans algo. to use same seed
randomstate = 12345678


def process_text(text,stem=True):
    """ Tokenize text and stem words removing punctuation """
    stop_words = set(stopwords.words('english'))
        
    text = text.translate("None")
    text = re.sub('can\'t', 'can not', text)
    text = re.sub('n\'t', ' not', text)
    text = re.sub(' da ', ' directaccess ', text)
    text = re.sub('direct access', 'directaccess', text)
    text = re.sub(r'[^\w]', ' ', text)

    tokens = word_tokenize(text)
    punctuation = re.compile(r'[-.?!,":;()|0-9]')

    tokens = [punctuation.sub("",w) for w in tokens]
    tokens = [w for w in tokens if not w in stop_words]
    tokens = [w for w in tokens if not w in stopwords_custom]
    tokens = [i for i in tokens if i not in string.punctuation]

    counter = 0
##    for i in tokens:
##        if i == 'da':
##            tokens[counter] = 'directaccess'
##        counter += 1   

    if stem:
        stemmer = SnowballStemmer("english")
        tokens = [stemmer.stem(t) for t in tokens]

    tokens = [w for w in tokens if not w in special_handling_words]
        
    return tokens

def cluster_texts(texts, idColumn = pd.DataFrame(columns=['ID']), numberOfClusters=3, maxNumberOfClusters = 3, numberOfWords = 5, minngrams = 1, maxngrams = 1, inputFileName = "survey.xlsx", filename = 'clust_sent.xlsx'):
            
    print(datetime.strftime(datetime.now(), '%H:%M:%S')+" Clustering Begins, Number of clusters = " + str(numberOfClusters))
    
    vectorizer = TfidfVectorizer(tokenizer=process_text,max_features=200000,
                                 stop_words=stopwords_custom,
                                 max_df=0.6,
                                 min_df=0.01,
                                 encoding = 'utf-16-le',
                                 ngram_range=(minngrams, maxngrams),
                                 decode_error = 'ignore'
                                 )

    tfidf_model = vectorizer.fit_transform(texts)
    # Get IDF values and feature names
    idf = vectorizer._tfidf.idf_
    terms = vectorizer.get_feature_names()

    indices = np.argsort(idf)[::-1]

    termsDictionary = collections.defaultdict(list)
    for t in range(0,len(terms)):
        termsDictionary[terms[t]] = idf[indices[t]]

    # Build KMeans model - need to re-iterate through kmeans model to ensure highest quality result is returned
    km_model = KMeans(n_clusters=numberOfClusters, init='k-means++', max_iter=100, random_state = randomstate).fit(tfidf_model)
    
    # ------------------------------------------------------------------------
    # Start: Record clusters and cluster information of each term
    labels= km_model.predict(tfidf_model)

    # Calculating Silhouette_avg a value between [-1, 1], the higher the better
    silhouette_avg = silhouette_score(tfidf_model, labels)

    clusters = {}
    surveyIds = {}

    n = 0
    termsClusterDictionary = collections.defaultdict(list)

    for item in labels:
        if item in clusters:
            clusters[item].append(texts[n])
            surveyIds[item].append(idColumn[n])
        else:
            clusters[item] = [texts[n]]
            surveyIds[item] = [idColumn[n]]
        n +=1

    order_centroids = km_model.cluster_centers_.argsort()[:, ::-1]
    # End: Record clusters and cluster information of each term
    # ------------------------------------------------------------------------
    # Start: Plotting clusters into 2 Dimensions (used pipeline before, with CountVectorizer...)
    X = tfidf_model.todense()

    pca = PCA().fit(X)
    #kmeans = KMeans(n_clusters=numberOfClusters, init='k-means++', max_iter=100, random_state = randomstate).fit(X)
    data2D = pca.transform(X)
    centers2D = pca.transform(km_model.cluster_centers_)#kmeans.cluster_centers_)
    #colors = pca.transform(km_model.labels_)

    D = cdist(data2D, centers2D, 'euclidean') 
    dist = np.min(D,axis=1)
    avgWithinSS = sum(dist)/data2D.shape[0]


    #pl.scatter(data2D[:,0], data2D[:,1], c=kmeans.labels_)
    #pl.hold(True)
    #pl.scatter(centers2D[:,0], centers2D[:,1], 
    #            marker='x', s=200, linewidths=3, c='r')
    #pl.savefig('Plot_'+inputFileName+'_NClust['+ str(numberOfClusters) +']_NWord['+ 
    #                             str(numberOfWords)+']_NGram['+str(maxngrams)+'].png')
    ########pl.show() 
    
    # End: Plotting clusters into 2 Dimensions    
    # ------------------------------------------------------------------------ 
    # Start: Count normalized words
    counterVectorizer = CountVectorizer(tokenizer=process_text,max_features=200000,
                                 stop_words=stopwords_custom,
                                 max_df=0.6,
                                 min_df=0.01,
                                 encoding = 'utf-16-le',
                                 ngram_range=(minngrams, maxngrams),
                                 decode_error = 'ignore'
                                 )
    
    # Get Frequency values and feature names
    tempData = counterVectorizer.fit_transform(texts).toarray()
    np.clip(tempData, 0 , 1, out = tempData)
    counterWords = np.sum(tempData, axis = 0)

    indicesCounter = np.argsort(counterWords)[::-1]

    counterTerms = counterVectorizer.get_feature_names()


    termsFrequencyDictionary = collections.defaultdict(list)
    for t in range(0,len(counterTerms)):
        termsFrequencyDictionary[counterTerms[t]] = counterWords[indicesCounter[t]]

    #word_freq_df = pd.DataFrame({'term': counterVectorizer.get_feature_names(), 'occurrences':np.asarray(counterVectorizer.fit_transform(texts).sum(axis=0)).ravel().tolist()})
    ##word_freq_df['frequency'] = word_freq_df['occurrences']/np.sum(word_freq_df['occurrences'])
    #print (word_freq_df.sort('occurrences',ascending = False))

    # End: Count normalized words
    # ------------------------------------------------------------------------ 
    if(numberOfClusters == maxNumberOfClusters-1):
        # Start: Plotting Term Frequency Dictionary
        sorted_termsFrequencyDictionary = OrderedDict(sorted(termsFrequencyDictionary.items(), key=lambda t: t[1], reverse = True))
    
        colorValue = list()
        for item in sorted_termsFrequencyDictionary:
            colorValue.append(termsClusterDictionary[item])

        x = np.arange(len(sorted_termsFrequencyDictionary))
        y = sorted_termsFrequencyDictionary.values()
        ax = pl.figure().add_subplot(111)
        pl.bar(x, y, color = 'blue')
        pl.xticks(x, sorted_termsFrequencyDictionary.keys(), rotation='vertical')
    
        ax.xaxis.set_ticks(range(len(sorted_termsFrequencyDictionary))[::10])
        pl.savefig(outputFolder+fileFolder+'BarPlot_'+inputFileName+'_NClust['+ str(numberOfClusters) +']_NWord['+ 
                                     str(numberOfWords)+']_NGram['+str(maxngrams)+'].png')
        #####pl.show()
        # End: Plotting Term Frequency Dictionary
    # ------------------------------------------------------------------------ 
    # to get top NumberOfWords terms per cluster 
    
    # Write results into output excel file
    
    print(datetime.strftime(datetime.now(), '%H:%M:%S')+" Writing to output file ")

    book = xlsxwriter.Workbook(outputFolder + fileFolder + 
                                files +'_NClust['+ str(numberOfClusters) +']_NWord['+ 
                                str(numberOfWords)+']_NGram['+str(maxngrams)+']_clust_sent.xlsx')
    
    # Summary of Clustering Results
    sheetSummary = book.add_worksheet('Summary_'+str(numberOfClusters))

    row = 0
    col = 0
    sheetSummary.write(row, 0, "Cluster_Index")
    sheetSummary.write(row, 1, "Cluster_Member")
    sheetSummary.write(row, 2, "Frequency")
    sheetSummary.write(row, 3, "TF_IDF")

    row += 1
    for i in range(numberOfClusters):
        sheetSummary.write(row, col, i+1)
        for ind in order_centroids[i, range(numberOfWords)]:
            termUnderStudy = terms[ind]
            sheetSummary.write(row, col + 1, termUnderStudy)
            sheetSummary.write(row, col + 2, termsFrequencyDictionary[termUnderStudy])
            sheetSummary.write(row, col + 3, termsDictionary[termUnderStudy])

            row += 1

    # Complete Clustering Results
    sheetComplete = book.add_worksheet('ClusteringResults_'+str(numberOfClusters))
    
    j=0
    sheetComplete.write(j, 0, "Cluster_Index")
    sheetComplete.write(j, 1, "ID")
    sheetComplete.write(j, 2, "English Comment")
    j += 1
    for item in clusters:
        #print (item+1 ," ,",end='')
        clustercounter = 0
        for i in clusters[item]:
            sheetComplete.write(j, 0, int(item+1))
            sheetComplete.write(j, 1, surveyIds[item][clustercounter])
            sheetComplete.write(j, 2, i)
            clustercounter += 1
            j += 1
  
    #if(numberOfClusters == maxNumberOfClusters-1):
    # Write terms and TF_IDF values
    sheetTF = book.add_worksheet('Term Frequencies')

    row = 0
    col = 0
    sheetTF.write(row, 0, "Term")
    sheetTF.write(row, 1, "Frequency")
    sheetTF.write(row, 2, "TF_IDF")
    
    
    row += 1
    for t in terms:
        sheetTF.write(row, col, t)
        sheetTF.write(row, col + 1, termsFrequencyDictionary[t])
        sheetTF.write(row, col + 2, termsDictionary[t])

        row += 1

    # To return clustering function       
    clustering = collections.defaultdict(list)
    for idx, label  in enumerate(km_model.labels_):
        clustering[label].append(idx)

    print()
    book.close()

    return clustering, avgWithinSS, silhouette_avg



##print(process_text("Dear Sirs,    Please update Memotech for the 3 matters listed below to reflect that the Workman Nydegger OC Attorney is Jonathan Richards and add the reference numbers as indicated below.     330953-WO-PCT - 13768.2560a    330953-CN-NP - 13768.2560b    330953-EP-EPT - 13768.2560a.1    Thank you,    Allyson Berri    Microsoft Patent Practice TeaPRIVACY: This e-mail may contain information that is privileged or confidential. If you are not the intended recipient, please delete the e-mail and any attachments and notify the sender immediately, and do not use, copy, or disclose to anyone any of the contents hereof."))



mydata = pd.DataFrame(columns=['English Comment'])
idColumn = pd.DataFrame(columns=['ID'])

for files in FileList:
    print(datetime.strftime(datetime.now(), '%H:%M:%S')+" Reading File "+ files)

    #con = pyodbc.connect('DRIVER={SQL Server};Server=dubcpdmsql08;Database=Workarea_MachineLearning;Trusted_Connection=yes;')
    con = pyodbc.connect('DRIVER={SQL Server};Server=kach-laptop;Database=Workarea;Trusted_Connection=yes;')
    cur = con.cursor()
    #cur.execute('SELECT [ID], [English Comment] AS TextForAnalysis FROM [Workarea_MachineLearning].[CPE].['+dbTableName+'] WHERE [English Comment] != \'\'')
    cur.execute('select top 5000 [ID], [description] as TextForAnalysis from [WORKAREA].[CUS].[SNOW_Incident_June2017_RAW1] where [description] is not null')
    rows = cur.fetchall()


    for row in rows:
        responses = row.TextForAnalysis
        id = row.ID
        mydata.loc[len(mydata)] = [responses]
        idColumn.loc[len(idColumn)] = [id]

    cur.close()
    con.close()


articles= mydata.squeeze()
idColumn = idColumn.squeeze()

print(datetime.strftime(datetime.now(), '%H:%M:%S')+" File Read")

avgWithinSS = []#collections.defaultdict(list)
silhouetteList = []

for n in range(numberOfClusters, maxNumberOfClusters+1):
    clusters, avgWithin, silhouette_avg = cluster_texts(articles, idColumn, n, maxNumberOfClusters, numberOfWords, minngrams, maxngrams, files, outputFolder + 
                                files +'_NClust['+ str(maxNumberOfClusters) +']_NWord['+ 
                                str(numberOfWords)+']_NGram['+str(maxngrams)+']_clust_sent.xlsx')
    avgWithinSS.append(avgWithin)
    silhouetteList.append(silhouette_avg)
        

book = xlsxwriter.Workbook(outputFolder + fileFolder + 
                                files +'_ElbowSil_NClust['+ str(maxNumberOfClusters) +']_NWord['+ 
                                str(numberOfWords)+']_NGram['+str(maxngrams)+']_clust_sent.xlsx')
# elbow curve
fig = pl.figure()
ax = fig.add_subplot(111)

x = range(numberOfClusters, maxNumberOfClusters+1)
y = avgWithinSS

pl.plot(x, y,'b*-')
pl.grid(True)
pl.xlabel('Number of clusters')
pl.ylabel('Average within-cluster sum of squares')
pl.title('Elbow for KMeans clustering')
pl.savefig(outputFolder+fileFolder+'ElbowMethod_'+files+'_MaxNClust['+ str(maxNumberOfClusters) +']_NWord['+ 
                        str(numberOfWords)+']_NGram['+str(maxngrams)+'].png')
pl.show()

# Difference between elements
jumpInAvgWithinSS = [abs(x - avgWithinSS[i - 1]) for i, x in enumerate(avgWithinSS)][1:]
N = len(jumpInAvgWithinSS)
x = range(numberOfClusters+1 , N + numberOfClusters+1)
width = 1/1.5
pl.bar(x, jumpInAvgWithinSS, width, color="blue")
pl.savefig(outputFolder+fileFolder+'JumpInAvgWithinSS_'+files+'_MaxNClust['+ str(maxNumberOfClusters) +']_NWord['+ 
                        str(numberOfWords)+']_NGram['+str(maxngrams)+'].png')
pl.show()

sheetElbow = book.add_worksheet('Elbow')
row = 0
col = 0
counterJump = 0

sheetElbow.write(row, col, "NumClust")
sheetElbow.write(row, col+1, "DecreaseInAvgWithinSS")
row += 1
for i in x:
    sheetElbow.write(row, col, i)
    sheetElbow.write(row, col+1, jumpInAvgWithinSS[counterJump])
    row += 1
    counterJump += 1

# silhouette plot
fig = pl.figure()
ax = fig.add_subplot(111)

x = range(numberOfClusters, maxNumberOfClusters+1)
y = silhouetteList

pl.plot(x, y,'b*-')
pl.grid(True)
pl.xlabel('Number of clusters')
pl.ylabel('Average Silhouette Score')
pl.title('Silhouette Results for KMeans clustering')
pl.savefig(outputFolder+fileFolder+'SilhouetteMethod_'+files+'_MaxNClust['+ str(maxNumberOfClusters) +']_NWord['+ 
                        str(numberOfWords)+']_NGram['+str(maxngrams)+'].png')
pl.show()

# writing silhouette results in excel
sheetSilhouette = book.add_worksheet('Silhouette')
row = 0
col = 0
counterJump = 0

sheetSilhouette.write(row, col, "NumClust")
sheetSilhouette.write(row, col+1, "Silhouette_Avg_Score")
row += 1
for i in x:
    sheetSilhouette.write(row, col, i)
    sheetSilhouette.write(row, col+1, silhouetteList[counterJump])
    row += 1
    counterJump += 1

book.close() 

