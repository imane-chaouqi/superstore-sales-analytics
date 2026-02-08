import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Superstore Analysis",
    layout="wide"
)

TURQUOISE = "#2A9D8F"

st.markdown("""
    <style>
        .stApp {
            background-color: #EDE4DA;
            color: #3A3A3A;
        }
        h1, h2, h3 {
            color: #2F2F2F;
        }
    </style>
""", unsafe_allow_html=True)

#Sidebar
st.sidebar.title("À propos")
st.sidebar.markdown("""
 **Portfolio Data Science - AI engineering student**  
Imane Chaouqi

🔗 [Code source sur GitHub](https://github.com/imane-chaouqi/superstore-sales-analytics)
""")


# Chargement des données
df = pd.read_csv("data/Sample-Superstore.csv", encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Titre & objectif
st.markdown("""
    <h1 style='text-align: center;'>From Data to Decisions :</h1>
""", unsafe_allow_html=True)
st.markdown("# Exploratory Data Analysis of Superstore Performance")
st.markdown("""
### Objectif du projet
Analyser les données de ventes afin d’évaluer la performance commerciale,
comprendre les facteurs clés de rentabilité et formuler des recommandations stratégiques basées sur l’analyse des données.
""")

# Aperçu des données
st.subheader("Aperçu des données")
st.write(df.head())

m1, m2 = st.columns(2)
m1.metric("Nombre de lignes", df.shape[0])
m2.metric("Nombre de colonnes", df.shape[1])

# BLOC 1 — RENTABILITÉ
col1, col2 = st.columns(2)

with col1:

     #Graphique Profit par catégorie
    st.subheader("Profit par catégorie")
    profit_by_category = df.groupby("Category")["Profit"].sum()
    fig, ax = plt.subplots(figsize=(5, 4))
    profit_by_category.plot(kind="bar", color=TURQUOISE, ax=ax)
    ax.set_xlabel("Catégorie")
    ax.set_ylabel("Profit")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("""**Insight :**
                 Les catégories Technology et Office Supplies sont les plus rentables
                 et surpassent largement la catégorie Furniture. Cela indique que ces
                 deux catégories constituent des leviers de croissance stratégiques et
                 devraient être priorisées dans les décisions d’investissement (gestion
                 des stocks, campagnes promotionnelles, partenariats) afin de maximiser
                 la rentabilité globale.""")

with col2:

     #Graphique Profit par sous-catégorie
    st.subheader("Profit par sous-catégorie")
    profit_by_subcategory = (
        df.groupby("Sub-Category")["Profit"]
        .sum()
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(5, 5))
    profit_by_subcategory.plot(kind="barh", color=TURQUOISE, ax=ax)
    ax.set_xlabel("Profit")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("""**Insight :**  
                L’analyse des sous-catégories met en évidence trois profils distincts : 
                des segments déficitaires (Tables, Bookcases, Supplies), des segments 
                faiblement performants mais avec potentiel de croissance, et des segments
                fortement rentables (Copiers, Phones, Accessories ). 
                Cette répartition suggère la nécessité de stratégies différenciées :
                actions correctives pour les pertes, optimisation pour les segments faibles,
                et stratégie de montée en charge (scaling) pour les sous-catégories à fort potentiel.""")

# BLOC 2 — CLIENTS & MARCHÉS
col3, col4 = st.columns(2)

with col3:

    # Graphique Ventes par segment client
    st.subheader("Ventes par segment client")
    sales_by_segment = df.groupby("Segment")["Sales"].sum()
    fig, ax = plt.subplots(figsize=(5, 4))
    sales_by_segment.plot(kind="bar", color=TURQUOISE, ax=ax)
    ax.set_xlabel("Segment")
    ax.set_ylabel("Ventes(millions $)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.1f}M')) # pour un format lisible en million 
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("""**Insight :** 
                Le segment Consumer génère la majorité du chiffre d’affaires.
                 Il constitue donc le cœur de l’activité et doit rester une
                 priorité stratégique. Toutefois, les segments Corporate et 
                Home Office représentent des opportunités de croissance,
                 notamment via des offres B2B ciblées et des programmes de 
                fidélisation adaptés.""")

with col4:

    # Graphique de Répartition des ventes par région
    st.subheader("Répartition des ventes par région")
    sales_by_region = df.groupby("Region")["Sales"].sum()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(
        sales_by_region,
        labels=sales_by_region.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig, use_container_width=True)

    st.markdown("""**Insight :**
                Les régions West et East concentrent la majorité 
                des ventes et constituent des marchés matures. 
                La région Central, avec près de 22 % des ventes,
                 représente un marché sous-exploité à fort potentiel 
                de croissance. La région South, plus faible, nécessite 
                des actions ciblées pour stimuler la demande.""")

# BLOC 3 — GÉOGRAPHIE & TEMPS
col5, col6 = st.columns(2)

with col5:

     # Graphique Top 10 États par ventes
    st.subheader("Top 10 États par ventes")
    top_states = (
        df.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    fig, ax = plt.subplots(figsize=(5, 5))
    top_states.plot(kind="barh", color=TURQUOISE, ax=ax)
    ax.set_xlabel("Ventes")
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("""**Insight :**
                California, New York et Texas génèrent
                la majorité des ventes, ce qui confirme
                leur rôle de marchés clés. Ces États 
                devraient bénéficier d’investissements 
                prioritaires (logistique, service client,
                stock). Toutefois, une analyse coût-bénéfice
                est nécessaire avant toute expansion physique.""")

with col6:

    # Graphique de l'évolution temporelle des ventes
    st.subheader("Évolution temporelle des ventes")
    sales_over_time = (
        df.set_index("Order Date")
        .resample("M")["Sales"]
        .sum()
    )
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(
        sales_over_time.index,
        sales_over_time.values,
        color=TURQUOISE,
        linewidth=2
    )
    ax.set_xlabel("Date")
    ax.set_ylabel("Ventes")
    plt.xticks(rotation=90)  # Dates affichées verticalement
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    st.markdown("""**Insight :**
                Les ventes présentent une forte saisonnalité 
                avec des pics en début et fin d’année. Ces 
                périodes doivent être exploitées via des 
                campagnes marketing intensives. En revanche,
                le milieu de l’année, plus faible, nécessite
                des actions promotionnelles pour stimuler la demande.""")

# Conclusion
st.subheader("Synthèse & pistes business")
st.markdown("""
À partir de l’analyse exploratoire et des visualisations, plusieurs axes d’amélioration ont été identifiés :
- Optimiser l’allocation des ressources vers les catégories les plus performantes
- Réduire l’impact des produits déficitaires via une révision de la stratégie produit
- Cibler prioritairement les segments clients et zones géographiques à fort potentiel
- Exploiter la saisonnalité pour maximiser l’efficacité des campagnes marketing 
""")

  





