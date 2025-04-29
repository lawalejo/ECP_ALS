# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración general de la app
st.set_page_config(page_title="Dashboard PRs", layout="wide")
st.title("📊 Dashboard de PRs - Requisition Date y Deletion Indicator")

# Subida del archivo
uploaded_file = st.file_uploader("🔼 Sube el archivo EXPORT_PO_..._COMPLETO.xlsx", type=["xlsx"])

if uploaded_file:
    # Leer archivo
    df = pd.read_excel(uploaded_file)
    df['Requisition Date'] = pd.to_datetime(df['Requisition Date'], errors='coerce')
    df['Year'] = df['Requisition Date'].dt.year
    df['Month'] = df['Requisition Date'].dt.month

    # Diccionario de meses
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    # ----------- SECCIÓN 1: Requisition Date -----------

    st.header("📆 Requisition Date por Año")

    requisition_summary = df.groupby(['Year', 'Month']).size().reset_index(name='Cantidad')
    years = sorted(requisition_summary['Year'].dropna().unique())
    selected_year = st.selectbox("Selecciona un año", years)

    data_year = requisition_summary[requisition_summary['Year'] == selected_year]
    fig, ax = plt.subplots(figsize=(10,6))
    bars = ax.bar(data_year['Month'], data_year['Cantidad'], color='#003366')

    ax.set_title(f'Requisition Dates por Mes - {selected_year}', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Mes')
    ax.set_ylabel('Cantidad de PRs')
    ax.set_xticks(data_year['Month'])
    ax.set_xticklabels([meses[m] for m in data_year['Month']], rotation=45)
    ax.set_ylim(0, data_year['Cantidad'].max() * 1.2)
    ax.grid(False)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 10),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

    st.pyplot(fig)

    # ----------- SECCIÓN 2: Deletion Indicator -----------

    st.header("🗑️ Deletion Indicator por Año")

    deletion_summary = df.groupby(['Year', 'Deletion indicator']).size().unstack(fill_value=0)

    fig2, ax2 = plt.subplots(figsize=(12, 8))
    deletion_summary.plot(
        kind='bar',
        stacked=True,
        color=['lightgreen', 'lightcoral'],
        edgecolor='black',
        ax=ax2
    )

    for container in ax2.containers:
        ax2.bar_label(container, label_type='center', fontsize=10, fontweight='bold')

    ax2.set_title('Distribución de Deletion Indicator por Año', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Año')
    ax2.set_ylabel('Cantidad de PRs')
    ax2.grid(False)
    ax2.legend(title='Deletion Indicator', title_fontsize='13', fontsize='11')

    st.pyplot(fig2)

else:
    st.info("⬆️ Sube un archivo Excel para comenzar.")
