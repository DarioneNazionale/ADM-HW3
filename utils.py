import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from math import log

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