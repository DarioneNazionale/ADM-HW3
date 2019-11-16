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

        plot = row[1]
        intro = row[2]

        preprocessed_data = preprocess(intro + plot)


        if len(vocabulary.keys()) == 0:
            vocabulary = dict([(x + 1, y) for x, y in enumerate(sorted(set(preprocessed_data)))])
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

# ----------> fuctions for compite the TFIDF <---------------
def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict


def computeIDF(documents):
    import math
    N = len(documents)

    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf
#------------------------------------------------------------


tfIdIndexDictionary = defaultdict(list)


for wordID in indexDictionary: #for each term in the indexDictionary:
    for fileNumber in indexDictionary[wordID]: #

        #fetch information on the tsv document
        with open('MoviesTSV\\article_' + str(fileNumber) + '.tsv', encoding='utf8') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            row = next(reader)

            #fetch intro and plot
            intro = row[1]
            plot = row[2]

            #process the data
            preprocessed_data = preprocess(intro + plot)

        #compute the tfdIdf
        tfIdf = computeTF(vocabulary[wordID], preprocessed_data)
        tfIdf = computeIDF(documents)

        # finally add the tfIdf to the dictionary
        tfIdIndexDictionary[wordID].append(tuple(fileNumber, tfIdf))