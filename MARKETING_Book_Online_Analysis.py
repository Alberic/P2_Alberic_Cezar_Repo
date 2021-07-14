import requests
from bs4 import BeautifulSoup
import prompt

def obtenir_url():
    url = prompt.string("URL :")
    assert url.startswith("http"), "L'url n'est pas valide"
    return url


def obtenir_page(url_page):
    page = requests.get(url_page)
    assert page.ok, "Impossible d'obtenir la page"
    return page


def parser_page(page_a_parser):
    texte_a_parser = page_a_parser.text
    page_parse = BeautifulSoup(texte_a_parser, "html.parser")
    return page_parse


test_url = obtenir_url()
test_page = obtenir_page(test_url)
test_parse = parser_page(test_page)
print(test_parse.text)
