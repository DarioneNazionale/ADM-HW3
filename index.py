import pickle
from collections import defaultdict
import os
import csv
import utils

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

        preprocessed_data = list(set(utils.preprocess(intro + " " + plot)))


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

#saving the indexDictionary in a file.
with open('indexDictionary.pkl', 'wb') as indexFile:
    pickle.dump(indexDictionary, indexFile, pickle.HIGHEST_PROTOCOL)

#saving the vocabulary in a file.
with open('vocabulary.pkl', 'wb') as indexFile:
    pickle.dump(vocabulary, indexFile, pickle.HIGHEST_PROTOCOL)



# ----------------------------------------> question 2.2.1 <----------------------------------------------

#Just creating the dict for the tfidf index
tfIdIndexDictionary = defaultdict(list)

for wordID in indexDictionary: #for each term in the indexDictionary:
    for fileNumber in indexDictionary[wordID]: #and for each document in the list:
        #fetch information on the tsv document
        with open('MoviesTSV\\article_' + str(fileNumber) + '.tsv', encoding='utf8') as tsvfile:
            reader = csv.reader(tsvfile, delimiter='\t')
            row = next(reader) #reading the file

            intro = row[1]
            plot = row[2]

            #fetch intro and plot
            articleContent = utils.preprocess(intro + " " + plot)

        # we try the code for just 10 elements for the moment
        tfIdf = utils.computeTfIdf(wordID, articleContent, vocabulary, indexDictionary, 10)

        # finally add the tfIdf to the dictionary
        tfIdIndexDictionary[wordID].append((fileNumber, tfIdf))


#debbug prints:
print(vocabulary)
print(tfIdIndexDictionary)

#saving the tfIdIndexDictionary in a file.
with open('tfIdIndexDictionary.pkl', 'wb') as tfIdIndexFile:
    pickle.dump(tfIdIndexDictionary, tfIdIndexFile, pickle.HIGHEST_PROTOCOL)