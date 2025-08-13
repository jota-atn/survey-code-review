import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

script_dir = Path(__file__).parent

root_dir = script_dir.parent

infile = root_dir / "data" / "processed" / "responses_clean.csv"

st.set_page_config(page_title="Dashboard Pesquisa Code Review", layout="wide")
st.title("📊 Dashboard - Inteligência Emocional no Code Review")

if not infile.exists():
    st.error(f"Arquivo processado não encontrado: {infile}")
    st.stop()

df = pd.read_csv(infile)

st.sidebar.header("Filtros")
vinculos = st.sidebar.multiselect("Vínculo com o curso", options=df['vinculo'].unique(), default=df['vinculo'].unique())
papeis = st.sidebar.multiselect("Papel no Code Review", options=df['participou_role'].unique(), default=df['participou_role'].unique())

filtered_df = df[df['vinculo'].isin(vinculos) & df['participou_role'].isin(papeis)]

st.subheader("📋 Estatísticas Descritivas")
st.write(filtered_df.describe())


st.subheader("📈 Distribuição das Respostas")
numeric_cols = filtered_df.select_dtypes(include=['int64', 'float64']).columns

for col in numeric_cols:
    st.markdown(f"**{col}**")
    fig, ax = plt.subplots()
    counts = filtered_df[col].value_counts().sort_index()
    ax.bar(counts.index, counts.values)
    ax.set_xlabel("Escala")
    ax.set_ylabel("Contagem")
    ax.set_xticks(counts.index)
    st.pyplot(fig)


st.subheader("🔗 Correlação entre Variáveis")
if not filtered_df[numeric_cols].empty:
    corr = filtered_df[numeric_cols].corr(method='spearman')
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)
else:
    st.warning("Não há dados numéricos para exibir correlação.")

st.success("✅ Dashboard gerado com sucesso!")
