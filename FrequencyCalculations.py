# Written by Daniel Rich

# FrequencyCalculations.py generates the knowledge base
# built by the scraping and crawling in Phase1
# the functions are called in Phase1.py and do not need to be run
# manually

# The api client key for aylien is located at the bottom

import os
import nltk
import re
from nltk.corpus import stopwords
import operator
import pickle
from aylienapiclient import textapi

def remove_stopwords(tokens):
    tokens = [word for word in tokens if word not in
              stopwords.words('english')]  # Remove stopwords
    return tokens

#Convert clean text files to NLTK Text Collection
def convertToTexts():
    print ("Converting clean files to text collection...")
    textList = []
    for filename in os.listdir(os.getcwd()):
        if "c_" in filename:
            file = open(filename, 'r', encoding='utf-8')
            text = file.read().lower()
            text = re.sub('[^\w\s]', ' ', text)
            tokens = nltk.word_tokenize(text)
            tokens = remove_stopwords(tokens)
            text = nltk.Text(tokens)
            textList.append(text)
            file.close()
    print("Finished converting clean files to Text collection")
    return [nltk.TextCollection(textList), textList]

#Make an API call to return the smmry
def getSmmry(url):
    summary = client.Summarize({'url': url, 'sentences_number': 3})
    return summary['sentences']


def buildKnowledgebase():

    returned_variables = convertToTexts()
    #Return the text list and the textCollection for packaging
    text_collection = returned_variables[0]
    texts = returned_variables[1]

    url_directory = open("directory.txt", "r")

    # Parse out titles, urls, filenames
    url_directory = url_directory.read()
    titles = re.findall('(?<=#title#)(.*)(?=#eotitle#)', url_directory)
    urls = re.findall('(?<=#urlstart#)(.*)(?=#urlend#)', url_directory)
    filenames = re.findall('(?<=#filestart#)(.*)(?=#fileend#)', url_directory)

    knowledge_base = {} # Article database
    words_to_articles = {} # Pointer database

    i = 0;
    for text in texts:
        print("Converting new article into knowledgebase...")
        filename = filenames[i]
        url = urls[i]
        title = titles[i]
        summary = getSmmry(url)
        important_words = {}

        # Get the importance value for every word in article
        for token in text:
            score = text_collection.tf_idf(token, text)
            important_words[token] = score

        # Get the top 10 most important
        most_important_words = dict(sorted(important_words.items(), key=operator.itemgetter(1), reverse=True)[:10])
        for item in most_important_words:
            words_to_articles.setdefault(item, [])
            words_to_articles[item].append(filename)

        knowledge_base[filename] = [title, url, most_important_words, summary]
        i = i + 1

        print("Done.")

        #Save pointer DB
    with open('words_to_articles.pickle', 'wb') as handle:
        pickle.dump(words_to_articles, handle, protocol=pickle.HIGHEST_PROTOCOL)

        #Save article DB
    with open('knowledge_base.pickle', 'wb') as handle:
        pickle.dump(knowledge_base, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return (knowledge_base, words_to_articles)

#Client key for Aylien api
client = textapi.Client("812fff2b", "a08d40d14c31e4f1f384d2941a18a0da")



