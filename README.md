# ADM-HW3
Repository for Homework3 ADM

Here you will find the total coding steps leading to a precise search between a data set of 30 000 different movies that allow a user to find the ones he is looking for regarding to a genre, a topic, a date or whatever he wants. 

On the first step named collector.py, we have created our own dataset using the 30000 wikipedia pages given. We have collected all the datas from 

On the second part : parser.py, we have used a function to transform the raw files form from HTML Wikipedia files to TSV files. We have extract specific informations from the HTML files such as the title, the introduction, the plot and the urls of each ones.

utils.py : on this python file is recorded some functions that we have used in the former files. Two functions are written :
      - the preprocess function : this function sorts all our data. It has 3 features : the first one is to remove every punctuation and lower all characteres. The second one remove all the english stopwords (according to a predefine list), and the last one stem all the words. 
      - the computeTfidf function : this function create the tfidf by multiplied the compued tf and computed idf created with the mathematical formulas. 

On the third step, index.py, python file that once executed generate the indexes of the Search engines. 


The exercise_4.py is a pyton code that finds the length of the longest palindromic substring of a string. We have used a dynamic way to resolve it putting succesively the answers of the substrings starting from a substring length equal to 1. 

