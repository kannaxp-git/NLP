##def lambda_unpack(f):
##return lambda args: f(*args)

#python 2.7 compatible

def extract_candidate_chunks(text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}'):
    import itertools, nltk, string
    
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize, POS-tag, and chunk using regular expressions
    chunker = nltk.chunk.regexp.RegexpParser(grammar)
    tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
    all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                    for tagged_sent in tagged_sents))
    # join constituent chunk words into a single chunked phrase
    candidates = [' '.join(word for word, pos, chunk in group).lower()
    for key, group in itertools.groupby(all_chunks, lambda(word,pos,chunk): chunk != 'O') if key]

##    candidates = [' '.join(word for word, pos, chunk in group).lower()
##                  for key, group in itertools.groupby(all_chunks, lambda_unpack(lambda word, pos, chunk: chunk != 'O')) if key]
##    
    return [cand for cand in candidates
            if cand not in stop_words and not all(char in punct for char in cand)]


print(extract_candidate_chunks("kannan works in microsoft, his role is data and applied scientist"))

##
##def extract_candidate_words(text, good_tags=set(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])):
##    import itertools, nltk, string
##
##    # exclude candidates that are stop words or entirely punctuation
##    punct = set(string.punctuation)
##    stop_words = set(nltk.corpus.stopwords.words('english'))
##    # tokenize and POS-tag words
##    tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent)
##                                                                    for sent in nltk.sent_tokenize(text)))
##    # filter on certain POS tags and lowercase all words
##    candidates = [word.lower() for word, tag in tagged_words
##                  if tag in good_tags and word.lower() not in stop_words
##                  and not all(char in punct for char in word)]
##
##    return candidates
##
##
##print(extract_candidate_words("kannan works in microsoft, his role is data and applied scientist"))


##def score_keyphrases_by_tfidf(texts, candidates='chunks'):
##    import gensim, nltk
##    
##    # extract candidates from each text in texts, either chunks or words
##    if candidates == 'chunks':
##        boc_texts = [extract_candidate_chunks(text) for text in texts]
##    elif candidates == 'words':
##        boc_texts = [extract_candidate_words(text) for text in texts]
##    # make gensim dictionary and corpus
##    dictionary = gensim.corpora.Dictionary(boc_texts)
##    corpus = [dictionary.doc2bow(boc_text) for boc_text in boc_texts]
##    # transform corpus with tf*idf model
##    tfidf = gensim.models.TfidfModel(corpus)
##    corpus_tfidf = tfidf[corpus]
##    
##    return corpus_tfidf, dictionary
##
##print(score_keyphrases_by_tfidf("kannan works in microsoft, his role is data and applied scientist"))
