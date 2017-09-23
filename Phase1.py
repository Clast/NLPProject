import string
from nltk.corpus import stopwords
import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import os
import nltk


def getImportantWords(numberofwords):
    print("Generating important words...")
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
            if len(lengths) < numberofwords:
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
                        for i in range(0, numberofwords):
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
    print("Top %d terms from all pages: " % numberofwords)
    for i in range(0, numberofwords):
        print(i, keys[i], " = ", lengths[i])
    return keys


def crawlAndReturnURLs(numOfMaxCrawls):
    print("Starting URL Crawl...")

    def words_in_string(word_list, a_string):
        for word in word_list:
            m = re.search(word, a_string)
            if m is not None:
                return True

    starter_url = "http://utdmercury.com/category/news/"
    URLs = {}
    numOfCrawls = 0
    URLList = []
    while (numOfCrawls < numOfMaxCrawls):

        r = requests.get(starter_url)

        data = r.text
        soup = BeautifulSoup(data)

        # write urls to a file
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            if link_str.__contains__("http"):
                # print(link_str)
                writable_link = str(link.get('href'))
                if writable_link not in URLList:
                    if "/category/" not in writable_link:
                        URLList.append(writable_link)
                if link_str.__contains__("news/page"):
                    if not URLs.__contains__(link_str):
                        URLs.setdefault(link_str, 0)

        for k in URLs:
            if URLs[k] == 0:
                URLs[k] = 1
                starter_url = k
                break;

        numOfCrawls = numOfCrawls + 1
    URLListFinal = []
    badWords = ["facebook.com", "twitter.com", "youtube.com", "/comics/", \
                "/eeditions-2", "/contact-us/", "/advertising", "/source-faqs/", "/author", \
                "instagram", "maps.google"]
    for k in URLList:
        if words_in_string(badWords, k):
            continue
        else:
            URLListFinal.append(k)
    print("Finished crawling.")
    return URLListFinal


def scrapeWeb(urllist):
    print("Starting to web scrape...")
    i = 0
    dire = open("directory.txt", "w+")
    for web in urllist:
        #mercury_web = list_html[web]
        page = urllib.request.urlopen(web)
        soup = BeautifulSoup(page)
        titlestr = soup.find("h1", "title entry-title")
        titlestr2 = re.sub("<.*?>", "", str(titlestr))
        titlestr2 = titlestr2.lstrip()
        f = open("d_%02d.txt" % i, "w+")
        dire.write("#title#%s#eotitle##filestart#c_%02d.txt$fileend$#urlstart#%s#urlend#\n" % (titlestr2, i, web))
        tmpstring = soup.prettify().encode('utf-8').decode('ascii', 'ignore')
        f.write(tmpstring)
        f.close()
        i += 1
    print("Done scraping")
    dire.close()


def cleanUp():
    print("Starting text cleanup...")
    i = 0
    for filename in os.listdir(os.getcwd()):
        if "d_" in filename:
            cleantext = ""
            file = open(filename, 'r', encoding='utf-8')
            sample = file.read()
            f = open("c_%02d.txt" % i, "w+")
            soup = BeautifulSoup(sample, 'html.parser')
            content = soup.find_all(class_="postcontent content")
            if content is not None:
                if len(content) > 0:
                    for listitem in content:
                        for thingy in listitem.find_all(class_="g"):
                            thingy.decompose()
            soup = BeautifulSoup(str(content), 'html.parser')
            ourresults = soup.find_all('p')
            for result in ourresults:
                tmpstring = str(result)
                tmpstring2 = re.sub("<.*?>", " ", tmpstring)
                cleantext += tmpstring2
            cleantext = cleantext.replace("\n", " ")
            cleantext = cleantext.replace("\t", " ")
            cleantext = ' '.join(cleantext.split())
            tokens = nltk.sent_tokenize(cleantext)
            for thingy in tokens:
                tmpstring = thingy.encode('utf8').decode('ascii', 'ignore')
                f.write("%s " % tmpstring)
            i += 1
            f.close()
        print("Finished cleaning")


def getTopWordsperFile():  # this function returns a list where each spot on the list is another list of top words in each file
    topwords = []
    exclude = set(string.punctuation)
    stopWords = set(stopwords.words('english'))
    for filename in os.listdir(os.getcwd()):
        if "c_" in filename:
            tmplist = []  # this stores the current file's name and top words
            tmplist.append(str(filename))
            file = open(filename, 'r', encoding='utf-8')
            text = file.read()
            altered_text = text.lower()
            altered_text = altered_text.replace("/n", " ")
            altered_text = ''.join(ch for ch in altered_text.replace("/n", " ") if ch not in exclude)
            tokens = nltk.word_tokenize(altered_text)
            removed_stopwords = []
            for word in tokens:
                if word not in stopWords:
                    removed_stopwords.append(word)
            filereq = nltk.FreqDist(removed_stopwords)  # this is the file's total frequency
            for tuple in filereq.most_common():  # adds the most common word to the tmplist
                tmplist.append(tuple[0])
            topwords.append(tmplist)  # add the tmplist to the overall list
    return topwords


def getSentencesperFile():  # this function returns a list of a list of sentences per file
    sentences = []
    for filename in os.listdir(os.getcwd()):
        if "c_" in filename:
            tmplist = []  # this stores the current file's name and sentences
            tmplist.append(str(filename))
            file = open(filename, 'r', encoding='utf-8')
            text = file.read()
            sentencetokens = nltk.sent_tokenize(text)
            for sent in sentencetokens:  # adds the most common word to the tmplist
                tmplist.append(str(sent))
            sentences.append(tmplist)  # add the tmplist to the overall list
    return sentences


def initializer():
    checkforfiles = 0  # checks if the program has been executed already; clean files must exist
    for filename in os.listdir(os.getcwd()):
        if "c_" in filename:
            checkforfiles += 1
    if checkforfiles == 0:
        url_list = crawlAndReturnURLs(10)
        scrapeWeb(url_list)
        cleanUp()
        getImportantWords(40)


def main():
    sentences = []
    topwords = []
    exclude = set(string.punctuation)
    stopWords = set(stopwords.words('english'))
    initializer()
    topwords = getTopWordsperFile()
    sentences = getSentencesperFile()
    inputstr = ""
    while inputstr != ".":
        inputstr = str(input("What is your question? Enter a period to exit. \n"))
        if inputstr != ".":
            count = [int(0)]*len(topwords)  # this keeps track of the matches
            indexcount = 0
            maxmatches = -9999  # this keeps track of the max matches
            maxmatchesindex = 0     # and this keeps track of where it is, since the index will correlate to the files
            relevantsentences = []  # this keeps track of relevant sentences containing the key word we want to print out
            altered_text = inputstr.lower()
            altered_text = altered_text.replace("/n", " ")
            altered_text = ''.join(ch for ch in altered_text.replace("/n", " ") if ch not in exclude)
            tokens = nltk.word_tokenize(altered_text)
            removed_stopwords = []
            for word in tokens:
                if word not in stopWords:
                    removed_stopwords.append(word)
            # now we compare the user's words to the top words and see which file we need to get
            for lists in topwords:
                for word in removed_stopwords:
                    if word in lists:
                        count[indexcount] += int(1)
                if maxmatches < count[indexcount]:
                    maxmatches = count[indexcount]
                    maxmatchesindex = indexcount
                indexcount += 1
            # at this point, we should know which file has the max number of matches so lets get the sentences of that file
            for sent in sentences[maxmatchesindex]:
                for word in removed_stopwords:
                    if str(word) in str(sent):
                        if str(sent) not in relevantsentences:
                            relevantsentences.append(str(sent))
            print("You should check out file %s. Relevant sentences might include: " % topwords[maxmatchesindex][0])
            for sent in relevantsentences:
                print(sent)

if __name__ == "__main__":
    main()








