import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

"""
Liste des fonctions :
- obtenir_page(arg) : Réalise un GET de l'url en argument.Retourne la page correspondante ou False s'il y a une erreur
- categorie_livre(arg) : Produit une liste des adresses de toutes les catégories sur la page passée en argument
- adresse_livres(arg) : Produit une liste des adresses de tous les livres présent sur la page passée en argument
- info_livre(arg) : Produit une liste de toutes les infos concernant le livre dont l'adresse a été fourni en argument
- toutes_les_pages(arg) : Produit une liste des adresses de toutes les pages d'une catégorie (adresse en argument)
"""

def obtenir_page(url_page):
    """
    Réalise un GET de l'url en argument et retourne la page correspondante ou False s'il y a une erreur
    :param url_page: url au format string
    :return: objet requests.Response de l'URL. En cas d'erreur, renvoie FALSE
    """
    page = requests.get(url_page)
    if page.ok:
        return page
    else:
        print('obtenir page - erreur')
        return False


def categorie_livre(page_a_parser):
    """
    Produit une liste des adresses de toutes les catégories présentent sur la page passée en argument
    :param page_a_parser: objet requests.Response de l'URL de la homepage
    :return: tableau des URL des catégories (premières pages) au format string
    """
    adresse_categorie = []
    page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
    for categorie in page_parse.findAll(href=re.compile("category")):
        base_adresse = page_a_parser.url
        base_adresse = base_adresse.rstrip('index.html')
        href = categorie.parent.a['href']
        adresse_categorie.append(base_adresse + href)
    return adresse_categorie


def adresse_livres(page_a_parser):
    """
    Produit une liste des adresses de tous les livres présent sur la page passée en argument
    :param page_a_parser: objet requests.Response d'une URL contenant des livres
    :return: tableau d'URL de livres au format string
    """
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
    """
    Produit une liste de toutes les infos concernant le livre dont l'adresse a été fourni en argument
    :param page_a_parser: objet requests.Response d'une URL de page de présentation d'un livre
    :return: dictionnaire de données concernant le livre
    """
    page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
    informations_tab = page_parse.findAll('td')
    description_soup = page_parse.find(class_= 'sub-header')
    rating_soup = page_parse.find("p", class_= "star-rating")
    category_soup = page_parse.findAll('a')
    image_soup = page_parse.find("img")
    url_parse = urlparse(page_a_parser.url)
    image_soup_string = str(image_soup.attrs.get('src'))
    extraction_info_title = {
        'product_page_url': page_a_parser.url,
        'universal_product_code': informations_tab[0].text,
        'title': page_parse.h1.text,
        'price_including_tax': informations_tab[3].text,
        'price_excluding_tax': informations_tab[2].text,
        'number_available': informations_tab[5].text,
        'product_description': description_soup.nextSibling.nextSibling.text,
        'category': category_soup[3].text,
        'review_rating': rating_soup.attrs.get('class')[1]+' out of Five stars',
        'image_url': url_parse.scheme+'://'+url_parse.netloc+'/'+image_soup_string.lstrip("./")
    }

    return extraction_info_title


def toutes_les_pages(page_a_parser):
    """
    Produit une liste des adresses de toutes les pages d'une catégorie dont l'adresse a été passé en argument
    :param page_a_parser: objet requests.Response de l'URL de la première page d'une catégorie
    :return: tableau de toutes les URL concernant la catégorie visée
    """
    liste_des_pages = [page_a_parser.url]
    page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
    p = 2
    url_parse = urlparse(page_a_parser.url)
    url_listed = url_parse.path.rsplit('/')
    url_listed.pop()

    while page_parse.find(class_='next') != None:
        nextpage = str(url_parse.scheme)+'://'+str(url_parse.netloc)+'/'+str(url_listed[1])+'/' +\
                   str(url_listed[2])+'/'+str(url_listed[3])+'/'+str(url_listed[4])+'/'+'page-'+str(p)+'.html'
        new_url = obtenir_page(nextpage)


        if new_url != False:
            page_parse = BeautifulSoup(new_url.content, "html.parser")
            liste_des_pages.append(new_url.url)
            p = p + 1
    cat_resultat = [str(url_listed[4]), liste_des_pages]
    return cat_resultat

def clean_texte(texte,liste_caractere):
    """
    Nettoie un texte en remplaçant les caractère non souhaités par des tirets
    :param texte: chaîne de caractère à nettoyer
    :param liste_caractere: liste des caractère à remplacer
    :return: chaîne de caractère modifiée
    """
    for caracteres in liste_caractere:
        texte = texte.replace(caracteres,'_')
    return texte
