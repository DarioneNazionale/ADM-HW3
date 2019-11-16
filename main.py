import pickle
import pandas as pd
import csv

with open('vocabulary.pkl', 'rb') as vocabularyFile:
    vocabulary = pickle.load(vocabularyFile)

with open('indexDictionary.pkl', 'rb') as indexFile:
    indexDictionary = pickle.load(indexFile)


# ----------------------------------------> question 2.1.2 <----------------------------------------------
search = input() #taken search elements from user

listOfsearchElements = search.split()
listOfsearchElements = list(dict.fromkeys(listOfsearchElements))  # removing repeating elements in a list

keyList = []
resultlist = []

listOfTitle = []
listOfIntro = []
listOfUrl = []

for i in range(len(listOfsearchElements)):
    for (key, value) in vocabulary.items():
        if value == listOfsearchElements[i]:  # check the search elements are in vocabulary dictionary , or not ?
            keyList.append(key)  # if they are exist in vocabulary dictionary , up them on keyList

if (len(keyList) != len(
        listOfsearchElements)):  # Being "len of key isnt equal to len of search list" mean is we cant research for all search element, so just quit to search
    print("Opps! Sorry we can't find any film")

if (len(keyList) == len(listOfsearchElements)):

    for j in range(len(keyList)):
        for (key, value) in indexDictionary.items():
            if key == keyList[j]:
                resultlist.append(value)

# compare for common articles
result = set(resultlist[0])
for s in resultlist[1:]:
    result.intersection_update(s)

result = list(result)
for i in range(len(result)):
    with open('MoviesTSV\\article_' + str(i) + '.tsv', encoding='utf8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        row = next(reader)

        title = row[0]
        intro = row[1]
        url = row[4]

        listOfTitle.append(title)
        listOfIntro.append(intro)
        listOfUrl.append(url)
        movies_df = pd.DataFrame({'Title': listOfTitle, 'Intro': intro, 'Url': url})
print(movies_df)


# ----------------------------------------> question 2.2.2 <----------------------------------------------