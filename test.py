from bs4 import BeautifulSoup
import requests

starter_url = "https://en.wikipedia.org/wiki/Vince_Gilligan"

r = requests.get(starter_url)

data = r.text
soup = BeautifulSoup(data)


# write urls to a file
with open('urls.txt', 'w') as f:
    for link in soup.find_all('a'):
        print(link.get('href'))
        f.write(str(link.get('href')) + '\n\n')

# end of program
print("end of crawler")