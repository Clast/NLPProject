# Swati Hirpara
# Write a function to clean up the text. You might need to delete newlines and tabs.
# Extract sentences with NLTK’s sentence tokenizer. Write the sentences for each file to a new file.
# That is, if you have 15 files in, you have 15 files out


import nltk
import string
import os
import re
import urllib.request
import bs4
from bs4 import BeautifulSoup

dir = "C:\\Users\\Swati\\PycharmProjects\\sample"
for filename in os.listdir(dir):
    with open(dir + '/' + filename, 'r') as f:
        sample = f.read()
        sample = sample.lower()

#list_html = ["http://utdmercury.com/peer-mentors-obtain-certification/","http://utdmercury.com/freshman-project-encourages-collaboration/","http://utdmercury.com/four-utd-alumni-killed-plano-home-mass-shooting/","http://utdmercury.com/relatives-friends-remember-victims-plano-shooting/","http://utdmercury.com/jsom-offers-new-beer-class/"]
#for web in list_html:
# #mercury_web = list_html[web]
# page = urllib.request.urlopen(web)
#soup = BeautifulSoup(page)
#  print(soup.prettify())
#clean up text

        cleantext = BeautifulSoup(raw_html).text
        cleantext = re.compile(r'<[^>]+>')
        def remove_tags(text):
                return TAG_RE.sub('', text)

        def cleanhtml(text):
                cleanr = re.compile('<.*?>')
                cleantext = re.sub(cleanr, '', text)
                return cleantext

    #def clean_up(text, strip_chars=[], replace_extras={}):
     #   clean_up_items = {'\n': ' ', '\r': ' ', '\t': ' ', '  ': ' '}
      #  clean_up_items.update(replace_extras)




