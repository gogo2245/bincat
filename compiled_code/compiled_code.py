from bs4 import BeautifulSoup
from requests import request

# Get links for all pages
page = request('GET', 'https://beginnersbook.com/2015/02/simple-c-programs/')
soup = BeautifulSoup(page.content, features='html.parser')
main_soup = soup.find('div', {'class': 'entry-content'})
links = []

for href_soup in main_soup.find_all('a', href=True)[1:-1]: #first and last links are irelevant
    links.append(href_soup['href'])

# Get code from page
for link in links:
    page = request('GET', link)
    soup = BeautifulSoup(page.content, features='html.parser')
    ffs = soup.find('pre')
    print(ffs.text) # TODO save code instead
