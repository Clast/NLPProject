# Chun's part of the project
# Write a function to extract at least 10 important terms
# from the pages using an importance measure such as term frequency.
# First, it’s a good idea to lower-case everything, remove stopwords and punctuation.
# Then build a vocabulary of unique terms.
# Create a dictionary of unique terms where the key is the token and the
# value is the count across all documents.
# Print the top 25-40 terms.
import sys
import os
import nltk
import string
from nltk.corpus import stopwords
def get_important_words():
    cwd = os.getcwd()
    lengths = []  # holds the 25 longest lengths
    keys = []  # holds the keys to the 25 longest lengths
    dictionary = {}  # holds all the unique words and their counts
    exclude = set(string.punctuation)
    stopWords = set(stopwords.words('english'))
    for filename in os.listdir(cwd):
        if "c_" in filename:
            file = open(filename, 'r')
            page_text = file.read()
            altered_text = page_text.lower()
            altered_text = altered_text.replace("/n", " ")
            altered_text = ''.join(ch for ch in altered_text.replace("/n", " ") if ch not in exclude)
            tokens = nltk.word_tokenize(altered_text)
            removed_stopwords = []
            for word in tokens:
                if word not in stopWords:
                    removed_stopwords.append(word)
            unique = set(removed_stopwords)
            freq = nltk.FreqDist(removed_stopwords)
            # builds or adds to dictionary
            for word in unique:
                if word not in dictionary:
                    dicttmp = {word: int(freq.get(word))}
                    dictionary.update(dicttmp)
                else:
                    dictionary[word] = dictionary[word] + int(freq.get(word))
            # builds the keys and lengths of the 25 longest lists
            if len(lengths) < 25:
                for key in dictionary:
                    lengths.append(dictionary[key])
                    keys.append(key)
            else:
            # then sort the 2 lists
                for key in dictionary:
                    if key not in keys:
                        smallestLength = 99999
                        smallestIndex = 99999
                        # gets the smallest length in the length list each time if the key isn't in list of keys
                        # switches out the smallest if it is smaller than dictionary at key
                        for i in range(0, 25):
                            if lengths[i] < smallestLength:
                                smallestLength = lengths[i]
                                smallestIndex = i
                        if smallestLength < dictionary[key]:
                            keys[smallestIndex] = key
                            lengths[smallestIndex] = dictionary[key]
                    else:
                        lengths[keys.index(key)] = dictionary[key]
            # sort the lengths and keys descending order
            for i in range(0, len(lengths)):
                maxL = lengths[i]
                maxI = i
                for j in range(i, len(lengths)):
                    if maxL < lengths[j]:
                        maxL = lengths[j]
                        maxI = j
                tmp = lengths[i]
                lengths[i] = maxL
                lengths[maxI] = tmp
                #sorts the keys associated with the lengths
                tmp = keys[i]
                keys[i] = keys[maxI]
                keys[maxI] = tmp
    print("Top 25 terms from all pages: ")
    for i in range(0, 25):
        print(i, keys[i], " = ", lengths[i])
    return keys
get_important_words()
