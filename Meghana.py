
import urllib.request
import bs4
from bs4 import BeautifulSoup
import requests
import re

dire = open("directory.txt", "w+")
def get_url_list(numOfMaxCrawls):

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
    return URLListFinal
def scrape(urllist = get_url_list(15)):
    i = 0
    for web in urllist:
        #mercury_web = list_html[web]
        page = urllib.request.urlopen(web)
        soup = BeautifulSoup(page)
        titlestr = soup.find_all("h1", "title entry-title")
        f = open("d_%02d.txt" % i, "w+")
        dire.write("%s - %s \n" % (titlestr, f.name))
        f.write(soup.prettify())
        f.close()
        i+=1
scrape()












