import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
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

def computeTfIdf(wordId, listOfStrings, vocabulary, indexDictionary, allFiles = 30000):

    tf = listOfStrings.count(vocabulary[wordId]) / len(listOfStrings)  # compute tf

    idf = 1.0 + log( allFiles / len(indexDictionary[wordId]))

    return tf * idf  # make the product to find the tfIdf


def CountCosineSimilarity(ListsearchTFIDF, ListdocumentTFIDF):
    dotProduct = 0
    for i in range(len(ListsearchTFIDF)):
        dotProduct = dotProduct + (ListsearchTFIDF[i] * ListdocumentTFIDF[i])

    queryNorm = 0
    for i in range(len(ListsearchTFIDF)):
        queryNorm += sqrt((ListsearchTFIDF[i]) * (ListsearchTFIDF[i]))

    documentNorm = 0
    for i in range(len(ListdocumentTFIDF)):
        documentNorm += sqrt((ListdocumentTFIDF[i]) * (ListdocumentTFIDF[i]))

    return (dotProduct / (queryNorm * documentNorm))
