from bo_def import obtenir_page, categorie_livre, adresse_livres, info_livre, toutes_les_pages, clean_texte
from pathlib import Path
import urllib.request
import csv
import re

def main():
    print("Démarrage du processus de scrapping")
    # Récupèrer les catégories de books.toscrape.com et supprimer la catégorie Book qui regroupe tous les livres
    url = obtenir_page("https://books.toscrape.com/index.html")
    liste_categorie = []
    for categories in categorie_livre(url):
        liste_categorie.append(categories)

    liste_categorie.pop(0)
    nombre_categorie = len(liste_categorie)
    print("Nombre de catégories à traiter : ", nombre_categorie )
    index_cat = 0

    # Pour chaque catégorie, identifier toutes les pages correspondantes et stocker dans liste_pages_par_categorie
    # et créér un fichier nom_categorie.csv avec des entêtes ses entêtes de colonnes colonnes
    print("avancement : ")
    while index_cat < len(liste_categorie):
        index_page = 0
        pages_categorie = obtenir_page(liste_categorie[index_cat])
        liste_pages_par_categorie = toutes_les_pages(pages_categorie)
        nom_categorie = str(liste_pages_par_categorie[0])
        base_path = Path('.')
        categorie_path = base_path / nom_categorie
        images_path = categorie_path / 'images'
        categorie_path.mkdir(exist_ok=True)
        images_path.mkdir(exist_ok=True)
        print(chr(13), index_cat+1,'- - -',nom_categorie, end= " ")
        nom_categorie = nom_categorie+'.csv'
        fichier = categorie_path.joinpath(nom_categorie)


        with open(fichier,'a', newline='', encoding='UTF8') as file:
            entetes_colonnes = ['product_page_url',
                                'universal_product_code',
                                'title',
                                'price_including_tax',
                                'price_excluding_tax',
                                'number_available',
                                'product_description',
                                'category',
                                'review_rating',
                                'image_url']
            writer = csv.DictWriter(file, fieldnames= entetes_colonnes)
            writer.writeheader()

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
                        livre_a_traiter = obtenir_page(ce_livre)
                        livre_info = info_livre(livre_a_traiter)

                        titre = livre_info.get("title")
                        nom_image = titre
                        url_image = livre_info.get("image_url")
                        description = livre_info.get('product_description')



                        caractere_interdit_csv = ['\'','"','‽','⸘','⸮',',','\\']

                        description = clean_texte(description, caractere_interdit_csv)
                        titre = clean_texte(titre, caractere_interdit_csv)
                        livre_info['product_description'] = description
                        livre_info['title'] = titre

                        writer.writerow(livre_info)


                        """
                        1-Longueur maximale du chemin d'accès complet à un fichier : 260 caractères
                    
                        2-Caractère Interdit pour les noms de fichier :
                        
                        < (plus petit que; less than)
                        > (plus grand que; greater than)
                        : (deux points; colon)
                        " (double appostrophe; double quote)
                        / (slash; barre de fraction; forward slash)
                        (antislash; backslash)
                        | (barre verticale; vertical bar; pipe)
                        ? (point d'interrogation; question mark)
                        * (astérisque; asterisk)
                        ‽ ⸘ interrobang and reverse interrobang
                        ⸮ point d'interrogation ironique
                        
                        """
                        caractere_interdit_image = ['<','>',':','"','/','\\','|','|','?','*','‽','⸘','⸮']
                        nom_image = clean_texte(nom_image,caractere_interdit_image)
                        nom_image = nom_image[0:100]
                        nom_image = nom_image+'.jpg'

                        image = images_path.joinpath(nom_image)
                        with urllib.request.urlopen(url_image) as data_handler:
                            image.write_bytes(data_handler.read())



                # Passer à la page suivante
                index_page = index_page + 1

        # Fermer le fichier une fois toutes les informations collectées
        #fichier.close()

        # Passer à la catégorie suivante
        index_cat = index_cat + 1

main()
