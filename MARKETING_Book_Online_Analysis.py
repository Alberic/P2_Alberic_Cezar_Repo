import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


def obtenir_page(url_page):
    page = requests.get(url_page)
    if page.ok:
        return page
    else:
        return False


def categorie_livre(page_a_parser):
    adresse_categorie = []
    page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
    for categorie in page_parse.findAll(href=re.compile("category")):
        base_adresse = page_a_parser.url
        base_adresse= base_adresse.rstrip('index.html')
        href = categorie.parent.a['href']
        adresse_categorie.append(base_adresse + href)
    return adresse_categorie

def adresse_livres(page_a_parser):
    adresse_livre = []
    page_parse = BeautifulSoup(page_a_parser.text, "html.parser")
    page_home_parse = urlparse(page_a_parser.url, 'http')
    page_home = page_home_parse.scheme+'://'+page_home_parse.netloc+'/'+'catalogue/'
    livre = page_parse.findAll('h3')
    for title in livre:
        href = str(title.a['href'])
        adresse_livre.append(page_home + href.lstrip("/."))
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

def toute_les_pages(page_a_parser):
     liste_des_pages=[page_a_parser.url]
     page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
     p = 2
     url_parse = urlparse(page_a_parser.url)
     url_listed = url_parse.path.rsplit('/')
     url_listed.pop()

     while page_parse.find(class_='next') != None:
         nextpage = str(url_parse.scheme)+'://'+str(url_parse.netloc)+'/'+str(url_listed[1])+'/'+str(url_listed[2])+'/'+str(url_listed[3])+'/'+str(url_listed[4])+'/'+'page-'+str(p)+'.html'
         new_url = obtenir_page(nextpage)

         if new_url != False:
             page_parse = BeautifulSoup(new_url.content, "html.parser")
             liste_des_pages.append(new_url.url)
             p = p + 1
     cat_resultat = [str(url_listed[4]), liste_des_pages]
     return  cat_resultat


url = obtenir_page("https://books.toscrape.com/index.html")
list_categorie_file = open('liste_categorie.txt', 'a')

liste_categorie = []
for categories in categorie_livre(url):
    liste_categorie.append(categories)

liste_categorie.pop(0)

index = 0
liste_pages_par_categorie = []
while index < len(liste_categorie):
    pages_categorie = obtenir_page(liste_categorie[index])
    print(toute_les_pages(pages_categorie))
    index = index + 1



list_categorie_file.writelines(liste_categorie)

"""liste_pages_categorie = []
for cat in liste_categorie:
    fichier_csv = open(cat+'.csv','c')
    url_cat = obtenir_page(cat)
    print(toute_les_pages(url_cat))"""