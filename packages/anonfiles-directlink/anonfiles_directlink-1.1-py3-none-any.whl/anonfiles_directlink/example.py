from bs4 import BeautifulSoup

def direct_link(p):
    soup = BeautifulSoup(requests.get(p).text, 'html.parser')
    for l in soup.find_all(id='download-url'):
        print(l['href'])
        return l['href']