import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

#charger les données 
df = pd.read_csv('data/Sample-Superstore.csv' , encoding='latin1')
print("Données chargées")

print(f"Lignes : {df.shape[0]} , Colonnes : {df.shape[1]}")

#Aperçu 
print("Les 5 premières lignes :")
print(df.head())

#Informations  
print("Informations sur les colonnes")
print(df.info())

#Statistiques  
print("Statistiques descriptives")
print(df.describe())

#  Nettoyage des données : 
# Nombre total de lignes
total_rows = df.shape[0]

#Nombre de lignes contenant au moins une valeur manquante
missing_rows = df.isnull().any(axis=1).sum()

# Seuil maximum autorisé pour la suppression des données(5%)
threshold  = 0.05*total_rows

if missing_rows <= threshold:
    df = df.dropna()
    print(f"{missing_rows} lignes supprimées (acceptable)")
else:
    print(f"{missing_rows} lignes manquantes (> seuil). Suppression annulée")

# Conversion des dates
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])


#Chiffre d’affaires total et profit total 
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()

print(f"Chiffres d'affaires total : {total_sales:.2f}")
print(f"Profit total : {total_profit:.2f}")

# Ventes par catégorie 
sales_by_category = df.groupby('Category')['Sales'].sum()
plt.figure()
sales_by_category.plot(kind='bar')
plt.title("Ventes par catégorie")
plt.ylabel("Ventes")
plt.xlabel("Catégorie")
plt.tight_layout()
plt.show()

#Profit par sous-catégorie (pour détecter les pertes)
profit_by_subcat = df.groupby('Sub-Category')['Profit'].sum().sort_values()

plt.figure()
profit_by_subcat.plot(kind='barh')
plt.title("Profit par sous-catégorie")
plt.xlabel("Profit")
plt.tight_layout()
plt.show()

#Ventes par région
sales_by_region = df.groupby('Region')['Sales'].sum()

plt.figure()
sales_by_region.plot(kind='pie' , autopct ='%1.1f%%')
plt.title("Répartition des ventes par région")
plt.ylabel("")
plt.tight_layout()
plt.show()

#Évolution des ventes dans le temps
sales_over_time = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum()
sales_over_time.index = sales_over_time.index.to_timestamp()

plt.figure()
plt.plot(sales_over_time)
plt.title("Évolution des ventes dans le temps")
plt.xlabel("Date")
plt.ylabel("Ventes")
plt.tight_layout()
plt.show()