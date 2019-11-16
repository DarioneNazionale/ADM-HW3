import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from math import log, sqrt

def preprocess(string):
    # Remove punctuation and lower all characters
    wordsList = nltk.word_tokenize(string)
    wordsList = [word.lower() for word in wordsList if word.isalnum()]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    wordsList = [i for i in wordsList if i not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    wordsList = [stemmer.stem(word) for word in wordsList]

    return wordsList

def computeTfIdf(wordId, listOfStrings, vocabulary, indexDictionary, allFiles = 30000):

    tf = listOfStrings.count(vocabulary[wordId]) / len(listOfStrings)  # compute tf

    idf = 1.0 + log( allFiles / len(indexDictionary[wordId])) # compute idf

    return tf * idf  # make the product to find the tfIdf


def CountCosineSimilarity(queryListsTFIDF, articleListTFIDF):

    #doing the dot product between articles and querys:
    dotProduct = 0
    for i in range(len(queryListsTFIDF)):
        dotProduct = dotProduct + (queryListsTFIDF[i] * articleListTFIDF[i])

    # find the norm of the query
    queryNorm = sum([sqrt((queryListsTFIDF[i]) * (queryListsTFIDF[i])) for i in range(len(queryListsTFIDF))])

    # find the norm of the article
    documentNorm = sum([sqrt((articleListTFIDF[i]) * (articleListTFIDF[i])) for i in range(len(articleListTFIDF))])

    return (dotProduct / (queryNorm * documentNorm)) #retun the cosin similarity: