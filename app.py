import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page web
st.set_page_config(page_title="Analyseur de Ventes", layout="centered")
st.title("📊 Analyse et Prévision des Ventes")
st.write("Importez votre fichier de ventes (CSV ou Excel) pour détecter les anomalies et projeter votre croissance.")

# 1. Bouton d'upload pour l'utilisateur
fichier = st.file_uploader("Glissez votre fichier ici (colonnes attendues : 'Jour' et 'Ventes_Euros')", type=["csv", "xlsx"])

# Option pour tester sans fichier (mode démonstration)
if fichier is None:
    st.info("💡 Aucun fichier importé. Affichage d'une démonstration avec des données fictives.")
    donnees = {
        'Jour': np.arange(1, 15),
        'Ventes_Euros': [1200, 1250, 1310, 1290, 1380, 1420, 410, 1490, 1530, 1580, 1610, 1650, 1700, 1740]
    }
    df = pd.DataFrame(donnees)
else:
    if fichier.name.endswith('.csv'):
        df = pd.read_csv(fichier)
    else:
        df = pd.read_excel(fichier)

# 2. Calculs statistiques
moyenne = df['Ventes_Euros'].mean()
ecart_type = df['Ventes_Euros'].std()
seuil_alerte = moyenne - 2 * ecart_type
anomalies = df[df['Ventes_Euros'] < seuil_alerte]

# Affichage des indicateurs clés
col1, col2, col3 = st.columns(3)
col1.metric("Moyenne / jour", f"{moyenne:.0f} €")
col2.metric("Écart-type", f"{ecart_type:.0f} €")
col3.metric("Anomalies détectées", len(anomalies))

# Alerte visuelle si une chute anormale est détectée
if not anomalies.empty:
    st.warning("⚠️ Attention : une baisse anormale des ventes a été détectée sur ces journées :")
    st.dataframe(anomalies, use_container_width=True)

# 3. Modélisation et curseur interactif de prévision
st.subheader("📈 Projection de croissance")
horizon = st.slider("Combien de jours dans le futur souhaitez-vous prédire ?", min_value=5, max_value=60, value=20)

df_propre = df[df['Ventes_Euros'] >= seuil_alerte]
a, b = np.polyfit(df_propre['Jour'], df_propre['Ventes_Euros'], 1)
jour_cible = df['Jour'].max() + horizon
prediction = a * jour_cible + b

st.success(f"Croissance estimée : **+{a:.2f} € / jour** — Prévision au Jour {jour_cible} : **{prediction:.2f} €**")

# 4. Affichage du graphique
fig, ax = plt.subplots(figsize=(8, 4))
ax.scatter(df['Jour'], df['Ventes_Euros'], color='#1f77b4', label='Ventes réelles')
ax.plot(df['Jour'], a * df['Jour'] + b, color='#d62728', linestyle='--', label='Tendance (Régression)')
ax.set_xlabel("Jour")
ax.set_ylabel("Chiffre d'affaires (€)")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)