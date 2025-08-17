import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

@st.cache_data
def load_data(file_path):
    if not file_path.exists():
        st.error(f"Arquivo de dados não encontrado: {file_path}")
        return pd.DataFrame()
    
    responses_analysis_df = pd.read_csv(file_path)
    return responses_analysis_df

def display_sidebar(responses_analysis_df):
    st.sidebar.header("Filtros")
    
    if responses_analysis_df.empty:
        st.sidebar.warning("Nenhum dado para filtrar.")
        return [], []

    vinculos = st.sidebar.multiselect(
        "Vínculo com o curso", 
        options=responses_analysis_df['vinculo'].unique(), 
        default=responses_analysis_df['vinculo'].unique()
    )
    papeis = st.sidebar.multiselect(
        "Papel no Code Review", 
        options=responses_analysis_df['participou_role'].unique(), 
        default=responses_analysis_df['participou_role'].unique()
    )
    return vinculos, papeis

def display_main_content(responses_analysis_df):
    st.subheader("📋 Estatísticas Descritivas")
    st.write(responses_analysis_df.describe())

    st.subheader("📈 Distribuição das Respostas")
    numeric_cols = responses_analysis_df.select_dtypes(include=['int64', 'float64']).columns

    for col in numeric_cols:
        st.markdown(f"**Análise da coluna: `{col}`**")
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.countplot(x=responses_analysis_df[col], ax=ax, palette="viridis")
        ax.set_xlabel("Escala")
        ax.set_ylabel("Contagem")
        st.pyplot(fig)

    st.subheader("🔗 Matriz de Correlação (Spearman)")
    if not responses_analysis_df[numeric_cols].empty and responses_analysis_df.shape[1] > 1:
        corr = responses_analysis_df[numeric_cols].corr(method='spearman')
        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
        st.pyplot(fig)
    else:
        st.warning("Não há dados suficientes para exibir a matriz de correlação com os filtros atuais.")

def main():
    st.set_page_config(page_title="Dashboard Pesquisa Code Review", layout="wide")
    st.title("📊 Dashboard - Inteligência Emocional no Code Review")

    file_path = Path(__file__).parent.parent / "data" / "processed" / "responses_clean.csv"
    
    responses_analysis_df_original = load_data(file_path)

    if responses_analysis_df_original.empty:
        st.stop()

    vinculos_selecionados, papeis_selecionados = display_sidebar(responses_analysis_df_original)

    filtered_responses_analysis_df = responses_analysis_df_original[
        responses_analysis_df_original['vinculo'].isin(vinculos_selecionados) & 
        responses_analysis_df_original['participou_role'].isin(papeis_selecionados)
    ]

    if filtered_responses_analysis_df.empty:
        st.warning("Nenhum dado corresponde aos filtros selecionados. Por favor, ajuste os filtros na barra lateral.")
    else:
        display_main_content(filtered_responses_analysis_df)

if __name__ == "__main__":
    main()