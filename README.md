 📚 Books Web Scraper - Data Collection from E-commerce

 🎯 Contexte et Objectif

 Problématique métier
Dans l'industrie du e-commerce, la collecte automatisée de données produits est essentielle pour :
- Veille concurrentielle : Surveillance des prix et disponibilités
- Analyse de marché : Compréhension de l'offre et positionnement
- Enrichissement de catalogues : Alimentation de bases de données produits

Ce projet démontre la capacité à extraire, structurer et transformer des données web non structurées en datasets exploitables.

 Objectifs du projet
- Développer un scraper web robuste pour extraire des données produits
- Collecter des informations structurées (titre, prix, disponibilité)
- Transformer les données HTML en format tabulaire (DataFrame)
- Démontrer la maîtrise des fondamentaux de la collecte de données

 🏗️ Architecture technique

 Stack technique
- Langage : Python 3.x
- Web Scraping : BeautifulSoup4, Requests
- Data Processing : Pandas
- Target : Site e-commerce de démonstration (books.toscrape.com)

 Pipeline de collecte

```
1. HTTP Request
   └─> GET request vers l'URL cible

2. HTML Parsing
   └─> BeautifulSoup parse le contenu HTML

3. Data Extraction
   ├─> Identification des sélecteurs CSS
   ├─> Extraction des titres (attribut 'title')
   ├─> Extraction des prix (class 'price_color')
   └─> Extraction des disponibilités (class 'instock availability')

4. Data Structuring
   └─> Construction de listes Python

5. Data Transformation
   └─> Conversion en DataFrame Pandas

6. Output
   └─> Dataset exploitable (CSV, Excel, base de données)
```

 Architecture du code

```
book_scraper.py
├── Imports (requests, BeautifulSoup, pandas)
├── Configuration (URL cible)
├── HTTP Request & Response handling
├── HTML Parsing (soup object)
├── Data Extraction Loop
│   ├── Title extraction
│   ├── Price extraction
│   └── Availability extraction
└── DataFrame Creation
```

 📊 Données collectées

 Structure du dataset

| Colonne | Type | Description | Exemple |
|---------|------|-------------|---------|
| `Title` | String | Titre complet du livre | "A Light in the Attic" |
| `Price` | String | Prix avec devise | "£51.77" |
| `Availability` | String | Statut de disponibilité | "In stock" |

 Volumétrie
- Page scrapée : 1 (page d'accueil)
- Produits par page : ~20 livres
- Taux de collecte : 100% (toutes les informations visibles)

 Exemple de données extraites

```
     Title                          Price    Availability
0    A Light in the Attic          £51.77   In stock
1    Tipping the Velvet            £53.74   In stock
2    Soumission                    £50.10   In stock
...
```

 🔍 Choix techniques

 Pourquoi BeautifulSoup et non Selenium ?

BeautifulSoup a été choisi car :
- ✅ Simplicité : Site statique sans JavaScript complexe
- ✅ Performance : Pas besoin de navigateur headless
- ✅ Légèreté : Moins de dépendances et ressources
- ✅ Rapidité : Parsing HTML direct vs rendu navigateur

Selenium serait nécessaire pour :
- Sites avec contenu chargé dynamiquement (React, Vue.js)
- Interactions complexes (scroll infini, clics, formulaires)
- Sites nécessitant JavaScript pour afficher le contenu

 Sélecteurs CSS utilisés

```python
# Article contenant un livre
'article.product_pod'

# Titre du livre (attribut HTML)
book.h3.a['title']

# Prix (class CSS)
'p.price_color'

# Disponibilité (class CSS composée)
'p.instock.availability'
```

Robustesse des sélecteurs :
- `class_='product_pod'` : Sélecteur stable lié à la structure du site
- Utilisation d'attributs HTML natifs (`title`) pour éviter les problèmes d'encodage
- `.text.strip()` pour nettoyer les espaces superflus

 🚀 Fonctionnalités implémentées

 1. Requête HTTP sécurisée
```python
response = requests.get(url)
# Note : Ajout de gestion d'erreur recommandé (voir Améliorations)
```

 2. Parsing HTML robuste
```python
soup = BeautifulSoup(response.content, 'html.parser')
# Parser 'html.parser' : plus rapide et sans dépendance externe
```

 3. Extraction multi-attributs
```python
for book in books:
    title = book.h3.a['title']           # Attribut HTML
    price = book.find('p', class_='price_color').text  # Texte d'élément
    availability = book.find('p', class_='instock availability').text.strip()
```

 4. Structuration des données
```python
data = {
    'Title': titles,
    'Price': prices,
    'Availability': availabilities
}
df = pd.DataFrame(data)
```

 📈 Résultats et Métriques

 Performance
- Temps d'exécution : < 2 secondes pour une page
- Taux de succès : 100% (site stable et prévisible)
- Données extraites : 20 livres par exécution

 Qualité des données
- Complétude : 100% (tous les champs remplis)
- Format : Données brutes (nettoyage requis pour le prix £)
- Cohérence : Structure identique pour tous les produits

 ⚠️ Limites et Améliorations futures

 Limites actuelles

1. Scraping mono-page
   - Une seule page collectée (20 livres)
   - Site contient 50 pages (1000 livres total)
   
2. Absence de gestion d'erreurs
   ```python
   # Problèmes potentiels non gérés :
   - Timeout de connexion
   - Erreur HTTP 404/500
   - Changement de structure HTML
   - Éléments manquants (livre sans prix)
   ```

3. Données non nettoyées
   - Prix en format string avec symbole £
   - Disponibilité avec texte superflu ("In stock")
   - Pas de conversion de types (price devrait être float)

4. Pas de respect des bonnes pratiques
   - Absence de `robots.txt` check
   - Pas de rate limiting (risque de ban)
   - User-Agent non défini
   - Pas de logs

5. Stockage temporaire
   - Données uniquement en mémoire (DataFrame)
   - Pas de persistance (CSV, base de données)

 Améliorations proposées

 ✅ Court terme (1-2 jours)

1. Pagination complète
```python
# Scraper toutes les pages (1-50)
for page in range(1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    # ... scraping logic
```

2. Gestion d'erreurs robuste
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Lève exception si 4xx/5xx
except requests.exceptions.RequestException as e:
    print(f"Erreur de requête : {e}")
```

3. Nettoyage des données
```python
# Conversion du prix en float
df['Price'] = df['Price'].str.replace('£', '').astype(float)

# Normalisation de la disponibilité
df['Availability'] = df['Availability'].apply(lambda x: 'In stock' if 'In stock' in x else 'Out of stock')
```

4. Export des données
```python
# Export CSV
df.to_csv('books_data.csv', index=False, encoding='utf-8')

# Export Excel (optionnel)
df.to_excel('books_data.xlsx', index=False)
```

 🔧 Moyen terme (1 semaine)

1. Configuration et bonnes pratiques
```python
# Headers pour simuler un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; BookBot/1.0)',
    'Accept': 'text/html,application/xhtml+xml'
}
response = requests.get(url, headers=headers)

# Rate limiting (respecter le site)
import time
time.sleep(1)  # 1 seconde entre chaque requête
```

2. Données enrichies
```python
# Extraire des informations supplémentaires :
- Note du livre (rating stars)
- Catégorie
- Image de couverture (URL)
- Lien vers la page détaillée
```

3. Logging structuré
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Scraping page {page}...")
logger.error(f"Échec extraction livre {title}")
```

4. Tests unitaires
```python
# Tester les fonctions d'extraction
def test_extract_title():
    sample_html = '<h3><a title="Test Book"></a></h3>'
    # ... assertions
```

 🚀 Long terme (1 mois)

1. Architecture modulaire
```python
# Séparation des responsabilités
class BookScraper:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def fetch_page(self, url):
        """Récupère le contenu d'une page"""
        pass
    
    def parse_books(self, soup):
        """Extrait les livres d'une page"""
        pass
    
    def clean_data(self, df):
        """Nettoie et transforme les données"""
        pass
    
    def save_to_db(self, df):
        """Sauvegarde en base de données"""
        pass
```

2. Base de données
```python
import sqlite3

# Stockage dans SQLite ou PostgreSQL
conn = sqlite3.connect('books.db')
df.to_sql('books', conn, if_exists='append', index=False)
```

3. Orchestration Airflow
```python
# DAG pour scraping quotidien
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(
    'books_scraper',
    schedule_interval='@daily',
    # ... configuration
)
```

4. Monitoring et alertes
```python
# Métriques de qualité
- Nombre de livres collectés par jour
- Taux d'erreur
- Temps d'exécution
- Alertes si site modifié (structure HTML changée)
```

5. API de données
```python
# Exposer les données via FastAPI
from fastapi import FastAPI

app = FastAPI()

@app.get("/books")
def get_books(min_price: float = 0, max_price: float = 100):
    # Retourner les livres filtrés
    pass
```

 🔒 Considérations légales et éthiques

 Bonnes pratiques de scraping

✅ À faire :
- Consulter le `robots.txt` du site
- Respecter les rate limits (1-2 sec entre requêtes)
- Utiliser un User-Agent identifiable
- Ne pas surcharger les serveurs (heures creuses)
- Respecter les CGU du site

❌ À éviter :
- Scraping intensif (DDoS involontaire)
- Contournement de mesures anti-scraping
- Revente de données scrapées sans autorisation
- Scraping de données personnelles (RGPD)

 Note légale
Ce projet est à but éducatif uniquement. Le site `books.toscrape.com` est un site de démonstration créé spécifiquement pour l'apprentissage du web scraping.

 📚 Compétences développées

 Techniques
- Web scraping : BeautifulSoup, sélecteurs CSS, parsing HTML
- HTTP requests : Gestion de requêtes, headers, responses
- Data wrangling : Manipulation de listes, transformation en DataFrame
- Python : Boucles, conditions, gestion de strings

 Méthodologiques
- Analyse de la structure HTML d'un site web
- Identification des sélecteurs CSS pertinents
- Gestion de données semi-structurées (HTML → DataFrame)
- Debugging d'extraction de données

 Domaine métier
- E-commerce : Compréhension des catalogues produits
- Data collection : Processus ETL (Extract, Transform, Load)
- Veille concurrentielle : Collecte automatisée de données marché

 🔧 Reproduction du projet

 Prérequis

```bash
# Python 3.7+
python --version

# Installation des dépendances
pip install beautifulsoup4
pip install requests
pip install pandas
```

Ou via `requirements.txt` :
```txt
beautifulsoup4==4.12.2
requests==2.31.0
pandas==2.1.0
```

```bash
pip install -r requirements.txt
```

 Utilisation

```bash
# Lancer le scraper
python book_scraper.py
```

Output attendu :
```
     Title                          Price    Availability
0    A Light in the Attic          £51.77   In stock
1    Tipping the Velvet            £53.74   In stock
...
```

 Structure du projet

```
book-scraper/
├── book_scraper.py          # Script principal
├── requirements.txt         # Dépendances Python
├── README.md               # Documentation
├── data/                   # (futur) Données collectées
│   └── books_data.csv
├── logs/                   # (futur) Logs d'exécution
└── tests/                  # (futur) Tests unitaires
    └── test_scraper.py
```

 🎓 Cas d'usage réels

Ce type de scraper peut être adapté pour :

1. E-commerce : Veille prix concurrence (Amazon, Cdiscount)
2. Immobilier : Collecte d'annonces (SeLoger, LeBonCoin)
3. Emploi : Agrégation d'offres d'emploi (LinkedIn, Indeed)
4. Actualités : Monitoring de news (Le Monde, Les Échos)
5. Réseaux sociaux : Analyse de tendances (via APIs officielles)

 📊 Extensions possibles

 1. Analyse de données
```python
# Statistiques sur les prix
df['Price_Clean'] = df['Price'].str.replace('£', '').astype(float)
print(f"Prix moyen : £{df['Price_Clean'].mean():.2f}")
print(f"Prix médian : £{df['Price_Clean'].median():.2f}")
```

 2. Visualisation
```python
import matplotlib.pyplot as plt

# Distribution des prix
df['Price_Clean'].hist(bins=20)
plt.title('Distribution des prix des livres')
plt.xlabel('Prix (£)')
plt.ylabel('Nombre de livres')
plt.show()
```

 3. Machine Learning
```python
# Prédiction de prix basée sur titre/catégorie
from sklearn.ensemble import RandomForestRegressor
# ... feature engineering + model training
```

 📖 Contexte académique

Projet réalisé dans le cadre : Master Data Engineer  
Cours : Web Scraping et Collecte de données  
Durée : 1 journée  
Objectif pédagogique : Maîtriser les fondamentaux du web scraping avec Python

 🔗 Ressources complémentaires

- [Documentation BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library](https://requests.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Web Scraping Best Practices](https://www.scrapehero.com/web-scraping-best-practices/)

 📧 Contact

Franck Ulrich BIPANDA  
📧 bipanda.franck@icloud.com  
🔗 [LinkedIn](https://linkedin.com/in/franck-bipanda-13392372)  
🌐 [Portfolio](https://datascienceportfol.io/bipandaf)

⭐ Si ce projet vous a été utile, n'hésitez pas à le star !
