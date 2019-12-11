# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 00:25:20 2018

@author: kach
"""
#
#from nltk.corpus import wordnet as wn
# 
#print(wn.synsets('cat', 'n'))
## [Synset('cat.n.01'), Synset('guy.n.01'), Synset('cat.n.03'), Synset('kat.n.01'), Synset('cat-o'-nine-tails.n.01'), Synset('caterpillar.n.02'), Synset('big_cat.n.01'), Synset('computerized_tomography.n.01')]
# 
#print(wn.synsets('dog', 'n'))
## [Synset('dog.n.01'), Synset('frump.n.01'), Synset('dog.n.03'), Synset('cad.n.01'), Synset('frank.n.02'), Synset('pawl.n.01'), Synset('andiron.n.01')]
# 
#print(wn.synsets('feline', 'n'))
## [Synset('feline.n.01')]
# 
#print(wn.synsets('mammal', 'n'))
## [Synset('mammal.n.01')]
# 
# 
## It's important to note that the `Synsets` from such a query are ordered by how frequent that sense appears in the corpus
## You can check out how frequent a lemma is by doing:
#cat = wn.synsets('cat', 'n')[0]     # Get the most common synset
#print(cat.lemmas()[0].count())       # Get the first lemma => 18
# 
#
#dog = wn.synsets('dog', 'n')[0]           # Get the most common synset
#feline = wn.synsets('feline', 'n')[0]     # Get the most common synset
#mammal = wn.synsets('mammal', 'n')[0]     # Get the most common synset
# 
#
## You can read more about the different types of wordnet similarity measures here: http://www.nltk.org/howto/wordnet.html
#for synset in [dog, feline, mammal]:
#    print("Similarity(%s, %s) = %s" % (cat, synset, cat.wup_similarity(synset)))
# 
## Similarity(Synset('cat.n.01'), Synset('dog.n.01')) = 0.2
## Similarity(Synset('cat.n.01'), Synset('feline.n.01')) = 0.5
## Similarity(Synset('cat.n.01'), Synset('mammal.n.01')) = 0.2
##----------------------------------------------------------------------------------------------------------------------------------------------------------------
 
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
 
def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
 
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
 
    score, count = 0.0, 0
 
    # For each word in the first sentence
    for synset in synsets1:
        # Get the similarity value of the most similar word in the other sentence
        best_score = max([synset.path_similarity(ss) for ss in synsets2])
 
        # Check that the similarity could have been computed
        if best_score is not None:
            score += best_score
            count += 1
 
    # Average the values
    score /= count
    return score
 
sentences = [
    "Dogs are awesome.",
    "Some gorgeous creatures are felines.",
    "Dolphins are swimming mammals.",
    "Cats are beautiful animals.",
]
 
focus_sentence = "Cats are beautiful animals."
 
for sentence in sentences:
    print("Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, sentence_similarity(focus_sentence, sentence)))
    print("Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, sentence_similarity(sentence, focus_sentence)))
    print("---------")
 
# Similarity("Cats are beautiful animals.", "Dogs are awesome.") = 0.511111111111
# Similarity("Dogs are awesome.", "Cats are beautiful animals.") = 0.666666666667
 
# Similarity("Cats are beautiful animals.", "Some gorgeous creatures are felines.") = 0.833333333333
# Similarity("Some gorgeous creatures are felines.", "Cats are beautiful animals.") = 0.833333333333
 
# Similarity("Cats are beautiful animals.", "Dolphins are swimming mammals.") = 0.483333333333
# Similarity("Dolphins are swimming mammals.", "Cats are beautiful animals.") = 0.4
 
# Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0
# Similarity("Cats are beautiful animals.", "Cats are beautiful animals.") = 1.0