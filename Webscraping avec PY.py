#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 09:43:21 2025

@author: macbook
"""

#libraries à installer 
!pip install BeautifulSoup4
!pip install requests

#libraries à importer
from bs4 import BeautifulSoup
import requests
import pandas as pd 

#url du site a scraper 
url='https://books.toscrape.com'

#effectuer une requete GET to recuperer le contenu de la page 
response = requests.get(url)

#parser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(response.content,'html.parser')

#trouver les éléments de livre
books = soup.find_all('article', class_='product_pod')

#installer la liste pour stocker les informations de livres
titles = []
prices = []
availabilities = []

#parcourir chaque livre et extraire les information souhaitées 
for book in books :
    
    #Titre du livre 
    title = book.h3.a['title']
    titles.append(title)

    #Prix du livre 
    price = book.find('p', class_='price_color').text
    prices.append(price)
    
    #Disponibilité
    availability = book.find('p', class_='instock availability').text.strip()
    availabilities.append(availability)
    
#Creer un dataFrame a partirdes listes
data = ({
        'Title': titles,
        'Price':prices,
        'Availability': availabilities
        })

#visualisation du dataframe 
df = pd.DataFrame(data)
df