import requests
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re


# Réalise un GET de l'url en argument et retourne la page correspondante ou False s'il y a une erreur
def obtenir_page(url_page):
    page = requests.get(url_page)
    if page.ok:
        return page
    else:
        print('obtenir page - erreur')
        return False


# Produit une liste des adresses de toutes les catégories présentent sur la page passée en argument
def categorie_livre(page_a_parser):
    adresse_categorie = []
    page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
    for categorie in page_parse.findAll(href=re.compile("category")):
        base_adresse = page_a_parser.url
        base_adresse = base_adresse.rstrip('index.html')
        href = categorie.parent.a['href']
        adresse_categorie.append(base_adresse + href)
    return adresse_categorie


# Produit une liste des adresses de tous les livres présent sur la page passée en argument
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


# Produit une liste de toutes les infos concernant le livre dont l'adresse a été fourni en argument
def info_livre(page_a_parser):

    page_parse = BeautifulSoup(page_a_parser.content, "html.parser")
    informations_tab = page_parse.findAll('td')
    description_soup = page_parse.find(class_='sub-header')
    rating_soup = page_parse.find("p", class_="star-rating")
    category_soup = page_parse.findAll('a')
    image_soup = page_parse.find("img")
    url_parse = urlparse(page_a_parser.url)
    image_soup_string = str(image_soup.attrs.get('src'))

    extraction_info_title = [
        page_a_parser.url,
        informations_tab[0].text,
        page_parse.h1.text,
        informations_tab[3].text,
        informations_tab[2].text,
        informations_tab[5].text,
        description_soup.nextSibling.nextSibling.text,
        category_soup[3].text,
        rating_soup.attrs.get('class')[1]+' out of Five stars',
        url_parse.scheme+'://'+url_parse.netloc+'/'+image_soup_string.lstrip("./")]

    return extraction_info_title


# Produit une liste des adresses de toutes les pages d'une catégorie dont l'adresse a été passé en argument
def toute_les_pages(page_a_parser):
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
        print('66- new_url', new_url.url)

        if new_url != False:
            page_parse = BeautifulSoup(new_url.content, "html.parser")
            liste_des_pages.append(new_url.url)
            p = p + 1
    cat_resultat = [str(url_listed[4]), liste_des_pages]
    print('categorie et pages associées : ', cat_resultat)
    return cat_resultat


# MAIN #

# Récupèrer les catégories de books.toscrape.com et supprimer la catégorie Book qui regroupe tous les livres
url = obtenir_page("https://books.toscrape.com/index.html")
liste_categorie = []
for categories in categorie_livre(url):
    liste_categorie.append(categories)

liste_categorie.pop(0)

index_cat = 0

# Pour chaque catégorie, identifier toutes les pages correspondantes et stocker dans liste_pages_par_categorie
# et créér un fichier nom_categorie.csv avec des entêtes ses entêtes de colonnes colonnes
while index_cat < len(liste_categorie):
    index_page = 0
    pages_categorie = obtenir_page(liste_categorie[index_cat])
    liste_pages_par_categorie = toute_les_pages(pages_categorie)
    nom_categorie = str(liste_pages_par_categorie[0])
    fichier = open(nom_categorie+'.csv', 'a', encoding='utf-8')
    entetes_colonnes = ["'product_page_url',",
                        "'universal_product_code',",
                        "'title',",
                        "'price_including_tax',",
                        "'price_excluding_tax',",
                        "'number_available',",
                        "'product_description',",
                        "'category',",
                        "'review_rating',",
                        "'image_url'"]
    fichier.writelines(entetes_colonnes)
    liste_pages_par_categorie.pop(0)

    # Pour chaque page de la catégorie
    while index_page < len(liste_pages_par_categorie):

        # Pour chaque page d'une catégorie, récupérer les adresses des livres et stocker dans livres
        for livre_par_categorie in liste_pages_par_categorie[index_page]:
            adresse_pages_par_categorie = obtenir_page(livre_par_categorie)
            livres = adresse_livres(adresse_pages_par_categorie)

            # Pour chaque livre, nettoyer les informations pour correspondre au format CSV
            # les écrire dans le fichier CSV et télécharger l'image
            for ce_livre in livres:
                fichier.write('\n')
                livre_a_traiter = obtenir_page(ce_livre)
                livre_info = info_livre(livre_a_traiter)
                url_image = livre_info[-1]
                urllib.request.urlretrieve(url_image, livre_info[2]+'.jpg')

                index_replace = 0
                while index_replace < len(livre_info):
                    livre_info[index_replace] = livre_info[index_replace].replace(',', '.')
                    livre_info[index_replace] = livre_info[index_replace].replace('"', '-')
                    index_replace = index_replace + 1

                for infos in livre_info:
                    fichier.write("\'"+infos+"\'"+',')

            # Passer à la page suivante
            index_page = index_page + 1

    # Fermer le fichier une fois toutes les informations collectées
    fichier.close

    # Passer à la catégorie suivante
    index_cat = index_cat + 1
