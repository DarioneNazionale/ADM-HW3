import pickle
import pandas as pd
import csv
from math import sqrt
import utils


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



#fetching the vocabulary from the file
with open('vocabulary.pkl', 'rb') as vocabularyFile:
    vocabulary = pickle.load(vocabularyFile)

#fetching the indexDictionary from the file
with open('indexDictionary.pkl', 'rb') as indexFile:
    indexDictionary = pickle.load(indexFile)

#debug prints:
print(indexDictionary)
print(vocabulary)
print(type(indexDictionary))
print(type(vocabulary))


searchEngine = int(input("select your search engine, only 2 available: "))

if searchEngine == 1:

    # ----------------------------------------> question 2.1.2 <----------------------------------------------
    query = utils.preprocess(input("query: ")) #taken search elements from user
    query = list(set(query))  # removing repeating elements in a list

    keyList = []
    for i in range(len(query)):
        for (key, value) in vocabulary.items():
            if value == query[i]:  # check the search elements are in vocabulary dictionary , or not ?
                keyList.append(key)  # if they are exist in vocabulary dictionary , up them on keyList



    if (len(keyList) == len(query)):

        resultlist = []
        for j in range(len(keyList)):
            for (key, value) in indexDictionary.items():
                if key == keyList[j]:
                    resultlist.append(value)

        # compare for common articles
        result = set(resultlist[0])
        for s in resultlist[1:]:
            result.intersection_update(s)

        listOfTitle = []
        listOfIntro = []
        listOfUrl = []
        result = list(result)
        for i in range(len(result)):
            with open('MoviesTSV\\article_' + str(i) + '.tsv', encoding='utf8') as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                row = next(reader)

                title = row[0]
                intro = row[1]
                url = row[3]

                listOfTitle.append(title)
                listOfIntro.append(intro)
                listOfUrl.append(url)
        movies_df = pd.DataFrame({'Title': listOfTitle, 'Intro': listOfIntro, 'Url': listOfUrl})
        print(movies_df)

    else:
        print("Opps! Sorry we can't find any film")

elif searchEngine == 2:
    # ----------------------------------------> question 2.2.2 <----------------------------------------------
    query = utils.preprocess(input("query: ")) #taken search elements from user

    #fetching the tfIdIndexDictionary from the file
    with open('tfIdIndexDictionary.pkl', 'rb') as tfIdIndexFile:
        tfIdIndexDictionary = pickle.load(tfIdIndexFile)

    # create the three dictionaries that stores:
    queryIds =  []# for each word of the query the number of times its repeted to the query
    articleTfIdfDict = dict() # for each word of the query the movies where it appears (and their tfIdf)
    articleList = [] # a list of lists where each list contains the movies that contain one of the words in the query
    for word in query:
        wordId = -1 # -1 means that we didn't find the wordId

        for (key, value) in vocabulary.items(): #serching the word id
            if value == word:  # check the search elements are in vocabulary dictionary , or not ?
                wordId = key  # if they are exist in vocabulary dictionary , up them on keyList
                break #we found it, we don't neet to look for it more

        if wordId == -1:  # if the wordId is not found that means that is a word not contained in any document
            break  # so we must stop

        queryIds.append(wordId)  # adding the count of the elements to queryDict
        articleTfIdfDict[wordId] = tfIdIndexDictionary[wordId]  # adding all the tuple movie, tfIdf to the articleTfIdfDict
        articleList.append(set(indexDictionary[wordId]))  # adding all the movies of that word to the articleList as sets

    if not wordId == -1: # we will do this operations only if all the words are contained in at last one article
        #finding common articles
        communArticles = list(set.intersection(*articleList))

        #updating the articleTfIdfDict, we must mantain only the common articles
        for wordId in articleTfIdfDict.keys():
            for tuple in articleTfIdfDict[wordId]:
                if tuple[0] not in communArticles:
                    articleTfIdfDict[wordId].remove(tuple)
    else:# we will do this operations only if all the words are contained in at last one article
        communArticles = []  # we initialize common articles as empty since we will not have articles in common


    #debug prints
    print(communArticles)
    print(articleTfIdfDict)
    print(queryIds)


    #"""
    if len(communArticles) > 0: #if a word in the query in not contained in any document we don't do anything else

        movies_df = pd.DataFrame()

        listOfTitle = []
        listOfIntro = []
        listOfUrl = []
        listOfSimilarity = []

        queryTfIdf = [utils.computeTfIdf(wordId, query, vocabulary, indexDictionary, 10) for ]


        for fileNumber in communArticles:

            with open('MoviesTSV\\article_' + str(fileNumber) + '.tsv', encoding='utf8') as tsvfile:
                reader = csv.reader(tsvfile, delimiter='\t')
                row = next(reader)

                title = row[0]
                intro = row[1]
                url = row[3]

                listOfTitle.append(title)
                listOfIntro.append(intro)
                listOfUrl.append(url)

            articleTfIdf = [articleTfIdfDict[wordId][1] for wordId in queryIds]

            listOfSimilarity.append(utils.CountCosineSimilarity(queryTfIdf, articleTfIdf))


        movies_df = pd.DataFrame({'Title': listOfTitle, 'Intro': listOfIntro, 'Url': listOfUrl, 'similarity': listOfSimilarity})
        print(movies_df.head())

    else:
        print("Opps! Sorry we can't find any film")
    #"""