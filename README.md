# Scrapper bookonline.py
Projet P2 - Books Online -
<body>

**Description du script**

Ce script est un scraper conçu pour le site https://books.toscrape.com

Il parcours chaque catégorie de livre sur le site afin de :

- créer un répertoire dédiée à la catégorie correspondante : "nom_de_catégorie"
- créer un fichier "nom_de_catégorie.csv" contenant les informations suivantes :
  - product_page_url
  - universal_ product_code (upc)
  - title
  - price_including_tax
  - price_excluding_tax
  - number_available
  - product_description
  - category
  - review_rating 
  - image_url
- télécharger les images de chaque livre de la catégorie dans le répertoire "nom_de_catégorie"\images\

**Environnement d'utilisation :** 

- Windows 10 Profesionnel
- Python 3.8.11

**Utilisation**

Les fichier suivants doivent être copier dans le même répertoire :
- bookonline.py
- bookonlinefonct.py
- requirements.txt

Pour lancer le programme de scrapping il est nécessaire de créer un environnement virtuel et d'y installer les librairies nécessaires à l'aide des commandes suivantes :

- python3 -m venv BookOnline
- BookOnline\Scripts\activate.bat
- python3 -m pip install -r requirements.txt

Une fois l'environnement configurer, lancer le programme :

- python3 -m bookonline.py


