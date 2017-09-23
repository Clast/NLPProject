import math
import os
import nltk
import re
from nltk.corpus import stopwords

#tfidf algorithm inspired by
#http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
#Re-written for use with nltk

def remove_stopwords(tokens):
    tokens = [word for word in tokens if word not in
              stopwords.words('english')]  # Remove stopwords
    return tokens

def convertToTexts():
    print ("Converting clean files to text collection...")
    textList = []
    for filename in os.listdir(os.getcwd()):
        if "c_" in filename:
            file = open(filename, 'r', encoding='utf-8')
            text = file.read()
            text = re.sub('[^\w\s]', ' ', text)
            tokens = nltk.word_tokenize(text)
            tokens = remove_stopwords(tokens)
            text = nltk.Text(tokens)
            textList.append(text)
            file.close()
    print("Finished converting clean files to Text collection")
    return [nltk.TextCollection(textList), textList]

returned_variables = convertToTexts()
text_collection = returned_variables[0]
texts = returned_variables[1]

print("test")

knowledge_base = {}
url_directory = open("directory.txt", "r")
url_directory = url_directory.read()
titles = re.findall('(?<=#title#)(.*)(?=#eotitle#)',url_directory)
urls = re.findall('(?<=#urlstart#)(.*)(?=#urlend#)',url_directory)
filenames = re.findall('(?<=#filestart#)(.*)(?=#fileend#)',url_directory)


for text in texts:
    print("Document: ")
    for token in text:
        score = text_collection.tf_idf(token,text)
        print("Word: " + token + " Score: " + str(score))

