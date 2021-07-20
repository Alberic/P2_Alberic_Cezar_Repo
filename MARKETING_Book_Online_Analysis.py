import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


def obtenir_page(url_page):
    page = requests.get(url_page)
    assert page.ok, "Impossible d'obtenir la page"
    return page


def categorie_livre(page_a_parser):
    adresse_categorie = []
    page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
    for categorie in page_parse.findAll(href=re.compile("category")):
        href = categorie.parent.a['href']
        adresse_categorie.append(page_a_parser.url + href)
    return adresse_categorie

def adresse_livres(page_a_parser):
    adresse_livre = []
    page_parse = BeautifulSoup(page_a_parser.text, "html.parser")
    livre = page_parse.findAll('h3')
    for title in livre:
        href = title.a['href']
        adresse_livre.append(page_a_parser.url + href)
    return adresse_livre

def info_livre(page_a_parser):
    page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
    informations_tab = page_parse.findAll('td')
    description_soup = page_parse.find(class_='sub-header')
    rating_soup = page_parse.find("p", class_="star-rating")
    category_soup = page_parse.findAll('a')
    image_soup = page_parse.find("img")
    url_parse = urlparse(page_a_parser.url)
    image_soup_string = str(image_soup.attrs.get('src'))

    extraction_info_title = dict(
        product_page_url = page_a_parser.url,
        universal_product_code = informations_tab[0].text,
        title = page_parse.h1.text,
        price_including_tax = informations_tab[3].text,
        price_excluding_tax = informations_tab[2].text,
        number_available = informations_tab[5].text,
        product_description  =  description_soup.nextSibling.nextSibling.text,
        category = category_soup[3].text,
        review_rating = rating_soup.attrs.get('class')[1]+' out of Five stars',
        image_url = url_parse.scheme+'://'+url_parse.netloc+'/'+image_soup_string.lstrip("./"),
    )
    print(extraction_info_title)


url = "https://books.toscrape.com/"
url_livre = "https://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"

page = obtenir_page(url)
livre = obtenir_page(url_livre)

adresses = adresse_livres(page)
categorie = categorie_livre(page)
datalivre = info_livre(livre)
#print(page.status_code)
#print(adresses)
#print (categorie)