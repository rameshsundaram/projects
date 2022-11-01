# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 13:48:08 2017

@author: ramsunda1
"""



import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
local_songs_data_path="C:\\Users\\ramsunda1\\Desktop\\Work\\Training\\spotify\\"

df_lyrics=pd.read_csv(local_songs_data_path+"TomPettyDS.csv", header=0, encoding='latin-1')
df_lyrics.columns
lyrics = df_lyrics['Lyrics_lyr'].values

vect = CountVectorizer(ngram_range=(2,2), stop_words='english')
X = vect.fit_transform(lyrics)
words = vect.get_feature_names()
#for word in words:
#    if(word.startswith("damage ve")):
#        print(word)

y = [int(x) for x in df_lyrics['Hit'].values]

clf = MultinomialNB(alpha=0)
clf.fit(X,y)

likelihood_df = pd.DataFrame(clf.feature_log_prob_.transpose(),columns=['Hit', 'Flop'], index=words)                

likelihood_df['Relative Prevalence for Hit'] = likelihood_df.eval('(exp(Hit) - exp(Flop))')

top_10 = likelihood_df['Relative Prevalence for Hit'].sort_values(ascending=False).ix[:10]

#Double-sorting here so that the graph will look nicer
bottom_10 = likelihood_df['Relative Prevalence for Hit'].sort_values().ix[:10].sort_values(ascending=False)

top_and_bottom_10 = pd.concat([top_10,bottom_10])
print(top_and_bottom_10)

import nltk
from collections import Counter
import string
def extract_phrases(text, phrase_counter, length):
    words = nltk.word_tokenize(text)
#    print(words)   
    for phrase in nltk.ngrams(words, length):
        if all(word not in string.punctuation for word in phrase):
            phrase_counter[phrase] += 1
                          
#raw_text = str(df_lyrics[df_lyrics.track_id=='5tVA6TkbaAH9QMITTQRrNv']['Lyrics_lyr'].values)
#raw_text="this is crazy, this is not crazy, but this would be crazy"
raw_text=df_lyrics['Lyrics_lyr'].str.cat()

#df_lyrics['common phrases']=df_lyrics['Lyrics_lyr'].apply(lambda x: extract_phrases())
#print(raw_text)

phrase_counter = Counter()
extract_phrases(raw_text, phrase_counter, 2)
most_common_phrases = phrase_counter.most_common(3)

for k,v in most_common_phrases:
    print ('{0: <5}'.format(v), k)
    
