#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import defaultdict
import os
import csv
from math import log


def preprocess(s):
    # Remove punctuation and lower all characters
    words = nltk.word_tokenize(s)
    words = [word.lower() for word in words if word.isalnum()]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [i for i in words if i not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]

    return words




# ----------------------------------------> question 2.1.1 <----------------------------------------------
vocabulary = dict()
indexDictionary = defaultdict(list)

fileNumber = 0  # starting from file 0
while os.path.exists("MoviesTSV\\article_" + str(fileNumber) + ".tsv"):  # Iterating for each file
    with open('MoviesTSV\\article_' + str(fileNumber) + '.tsv', encoding='utf8') as tsvfile:

        reader = csv.reader(tsvfile, delimiter='\t')
        row = next(reader)

        intro = row[1]
        plot = row[2]

        preprocessed_data = list(set(preprocess(intro + " " + plot)))


        if len(vocabulary.keys()) == 0:
            vocabulary = dict([(x + 1, y) for x, y in enumerate(preprocessed_data)])
        else:
            for word in preprocessed_data:
                if not word in vocabulary.values():
                    vocabulary[max(vocabulary.keys())] = word

        for index in vocabulary:
            if vocabulary[index] in preprocessed_data:
                indexDictionary[index].append(fileNumber)
                
        fileNumber += 1
        
        #This make the scrypt reate the index only for the first 10 files at most.

        if fileNumber == 10:
            break


with open('indexDictionary.pkl', 'wb') as indexFile:
    pickle.dump(indexDictionary, indexFile, pickle.HIGHEST_PROTOCOL)

with open('vocabulary.pkl', 'wb') as indexFile:
    pickle.dump(vocabulary, indexFile, pickle.HIGHEST_PROTOCOL)



# ----------------------------------------> question 2.2.1 <----------------------------------------------

#Just creating the dict for the tfidf index
tfIdIndexDictionary = defaultdict(list)

for wordID in indexDictionary: #for each term in the indexDictionary:
    for fileNumber in indexDictionary[wordID]: #and for each document in the list:
        print("----------------> file number: ", fileNumber)
        #fetch information on the tsv document
        with open('MoviesTSV\\article_' + str(fileNumber) + '.tsv', encoding='utf8') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            row = next(reader) #reading the file

            intro = row[1]
            plot = row[2]

            #fetch intro and plot
            articleContent = preprocess(intro + " " + plot)
            
            
        #-----------------> computing the tfdIdf <-----------------------
        tf = articleContent.count(vocabulary[wordID]) / len(articleContent) #compute tf

        if tf == 0:
            print("the tf is == 0, and the count of the words in this article is: ", articleContent.count(vocabulary[wordID]))
            print("we are looking for: ", vocabulary[wordID])
            print("the content is: ", articleContent)

        #nunning just for 10 files since we want to test it
        idf = 1.0 + log(10 / len(indexDictionary[wordID]))

        tfIdf = tf * idf #make the product to find the tfIdf
        #---------------------------------------------------------

        # finally add the tfIdf to the dictionary
        tfIdIndexDictionary[wordID].append((fileNumber, tfIdf))


#debbug prints:
print(vocabulary)
print(tfIdIndexDictionary)

#saving the tfIdIndexDictionary in a file.
with open('tfIdIndexDictionary.pkl', 'wb') as tfIdIndexFile:
    pickle.dump(tfIdIndexDictionary, tfIdIndexFile, pickle.HIGHEST_PROTOCOL)