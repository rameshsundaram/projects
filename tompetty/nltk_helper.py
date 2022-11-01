# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 13:07:35 2016

@author: Ramesh.Sundaram
"""
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
stop=stopwords.words('english')

def extract_meta_elements(document):
    sentences=nltk.sent_tokenize(document);    
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences
    
    
def word_tokenize(raw_text, remove_stop=True):
     tokenizer= RegexpTokenizer(r'[a-zA-Z]+')
     tokens=tokenizer.tokenize(raw_text)
     if remove_stop:
         sub_tokens_wo_stop=[w1 for w1 in tokens if w1 not in stop]
         return sub_tokens_wo_stop;
     return tokens
    
def lexical_diversity(nltk_text):
    return len(nltk_text)/len(set(nltk_text))

def percentage_word(nltk_text, word):
    return 100 * nltk_text.count(word) / len(nltk_text)


def words_per_sents(raw_text):
    words=word_tokenize(raw_text, False)    
    sents=nltk.sent_tokenize(raw_text)
#    print(words, sents)
    return len(words)/len(sents)

#Example Description
    #fdist = FreqDist(samples) Create a frequency distribution containing the given samples
    #fdist.inc(sample) Increment the count for this sample
    #fdist['monstrous'] Count of the number of times a given sample occurred
    #fdist.freq('monstrous') Frequency of a given sample
    #fdist.N() Total number of samples
    #fdist.keys() The samples sorted in order of decreasing frequency
    #for sample in fdist: Iterate over the samples, in order of decreasing frequency
    #fdist.max() Sample with the greatest count
    #fdist.tabulate() Tabulate the frequency distribution
    #fdist.plot() Graphical plot of the frequency distribution
    #fdist.plot(cumulative=True) Cumulative plot of the frequency distribution
    #fdist1 < fdist2 Test if samples in fdist1 occur less frequently than in fdist2
    
def plot_freq_dist(tokens,  plot_count=50):
        text=nltk.Text(tokens)            
        fdist=nltk.FreqDist(text)
        fdist.plot(plot_count)
    
    
def freq_dist_by_length(nltk_text):
    fdist = nltk.FreqDist([len(w) for w in nltk_text])
    print(fdist.items())
    fdist.keys()
    fdist.freq(3)
        
        
#        nltk_text.similar("expel")
#        nltk_text.common_contexts([ "expel"])
#        nltk_text.dispersion_plot(["maintain"])
#        len(nltk_text)    
#        nltk_text.collocations() #find words that collocate


from collections import Counter
import string
def extract_phrases(text, phrase_counter, length):
    words = nltk.word_tokenize(text)
#    print(words)   
    for phrase in nltk.ngrams(words, length):
        if all(word not in string.punctuation for word in phrase):
            phrase_counter[phrase] += 1
                          

raw_text="this is crazy, this is not crazy, but this would be crazy"
#print(raw_text)
phrase_counter = Counter()
extract_phrases(raw_text, phrase_counter, 2)
most_common_phrases = phrase_counter.most_common(3)
for k,v in most_common_phrases:
    print ('{0: <5}'.format(v), k)