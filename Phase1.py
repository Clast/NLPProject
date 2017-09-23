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
        dire.write("#title#%s#eotitle##filestart#c_%02d.txt#fileend##urlstart#%s#urlend#\n" % (titlestr2, i, web))
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




def main():
    url_list = crawlAndReturnURLs(4)
    scrapeWeb(url_list)
    cleanUp()
    #getImportantWords(40)

if __name__ == "__main__":
    main()









