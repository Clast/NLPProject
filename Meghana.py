import urllib.request
import bs4
from bs4 import BeautifulSoup

list_html = ["http://utdmercury.com/peer-mentors-obtain-certification/","http://utdmercury.com/freshman-project-encourages-collaboration/","http://utdmercury.com/four-utd-alumni-killed-plano-home-mass-shooting/","http://utdmercury.com/relatives-friends-remember-victims-plano-shooting/","http://utdmercury.com/jsom-offers-new-beer-class/"]
for web in list_html:
    #mercury_web = list_html[web]
    page = urllib.request.urlopen(web)
    soup = BeautifulSoup(page)
    print(soup.prettify())




