import requests
from bs4 import BeautifulSoup
import prompt

def obtenir_page(url_page):
    page = requests.get(url_page)
    assert page.ok, "Impossible d'obtenir la page"
    return page


def adresse_livres(page_a_parser):
    adresse_livre = []
    page_parse = BeautifulSoup(page_a_parser.text, "html.parser")
    livre = page_parse.findAll('h3')
    for title in livre:
        href = title.a['href']
        adresse_livre.append(page_a_parser.url + href)
    return adresse_livre


url = "https://books.toscrape.com/"
page = obtenir_page(url)
adresse = adresse_livres(page)
print(adresse)
