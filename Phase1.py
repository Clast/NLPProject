import string
from nltk.corpus import stopwords
import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import os
import nltk
import FrequencyCalculations
import pickle


def words_in_string(word_list, a_string):
    for word in word_list:
        m = re.search(word, a_string)
        if m is not None:
            return True

def crawlAndReturnURLs(num_of_max_crawls):

    print("Starting URL Crawl...")

    starter_url = "http://utdmercury.com/category/news/"
    navigation_urls = {}
    num_of_crawls = 0
    possible_articles = []
    while num_of_crawls < num_of_max_crawls:

        r = requests.get(starter_url)
        data = r.text
        soup = BeautifulSoup(data)

        #Keep track of navigation urls in navigation_urls and mark as visited
        #Keep possible articles in possible_articles
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            if link_str.__contains__("http"):
                # print(link_str)
                writable_link = str(link.get('href'))
                if writable_link not in possible_articles:
                    if "/category/" not in writable_link:
                        possible_articles.append(writable_link)
                if link_str.__contains__("news/page"):
                    if not navigation_urls.__contains__(link_str):
                        navigation_urls.setdefault(link_str, 0)

        #If not visited, visit on next loop
        for k in navigation_urls:
            if navigation_urls[k] == 0:
                navigation_urls[k] = 1
                starter_url = k
                break;

        num_of_crawls = num_of_crawls + 1

    #Parse out bad urls from the possible article list
    article_url_final = []
    bad_words = ["facebook.com", "twitter.com", "youtube.com", "/comics/", \
                "/eeditions-2", "/contact-us/", "/advertising", "/source-faqs/", "/author", \
                "instagram", "maps.google", "sg-report", "mercury-morning-news"]

    for k in possible_articles:
        if words_in_string(bad_words, k):
            continue
        else:
            article_url_final.append(k)
    print("Finished crawling.")
    return article_url_final


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
    FrequencyCalculations.buildKnowledgebase()
    print("Knowledgebase built. Pickle files ready to load.")
    print("Loading pickle files...DEBUG: Place a stop point on the print(complete) line to view knowledgebase")

    with open('knowledge_base.pickle', 'rb') as handle:
        knowledge_base = pickle.load(handle)

    with open('words_to_articles.pickle', 'rb') as handle:
        words_to_articles = pickle.load(handle)

    print("Complete")


if __name__ == "__main__":
    main()









