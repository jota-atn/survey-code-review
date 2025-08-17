import argparse
import logging
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sns.set_theme(style="whitegrid", palette="viridis")

def generate_bar_charts(responses_analysis_df, output_dir):
    numeric_cols = responses_analysis_df.select_dtypes(include=['int64', 'float64']).columns
    logging.info(f"Gerando {len(numeric_cols)} gráficos de barras...")
    
    for col in numeric_cols:
        plt.figure(figsize=(8, 5))
        counts = responses_analysis_df[col].value_counts().sort_index()
        
        ax = sns.barplot(x=counts.index, y=counts.values)
        ax.set_title(f"Distribuição de Respostas: '{col}'", fontsize=14)
        ax.set_xlabel("Escala de Resposta", fontsize=12)
        ax.set_ylabel("Contagem", fontsize=12)
        
        plt.xticks(ticks=range(len(counts.index)), labels=counts.index)
        plt.tight_layout()
        
        fig_path = output_dir / f"{col}_bar_chart.png"
        plt.savefig(fig_path, dpi=150, bbox_inches='tight')
        plt.close()
    logging.info("Gráficos de barras gerados com sucesso.")

def generate_correlation_heatmap(responses_analysis_df, output_dir):
    numeric_responses_analysis_df = responses_analysis_df.select_dtypes(include=['int64', 'float64'])
    
    if numeric_responses_analysis_df.shape[1] < 2:
        logging.warning("Não há colunas numéricas suficientes para gerar um heatmap de correlação.")
        return

    logging.info("Gerando heatmap de correlação...")
    corr = numeric_responses_analysis_df.corr(method='spearman')
    
    plt.figure(figsize=(12, 10))
    ax = sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=.5)
    ax.set_title("Matriz de Correlação (Spearman)", fontsize=16)
    
    plt.tight_layout()
    fig_path = output_dir / "correlation_heatmap.png"
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    logging.info("Heatmap de correlação gerado com sucesso.")

def create_visualizations(input_path, output_dir):
    logging.info(f"Iniciando geração de visualizações do arquivo: {input_path}")
    
    if not input_path.exists():
        logging.error(f"Arquivo de entrada não encontrado: {input_path}")
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_path}")

    try:
        responses_analysis_df = pd.read_csv(input_path)
        logging.info(f"Dados lidos com sucesso ({responses_analysis_df.shape[0]} linhas).")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        generate_bar_charts(responses_analysis_df, output_dir)
        generate_correlation_heatmap(responses_analysis_df, output_dir)

    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado durante a geração dos gráficos: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Gera visualizações a partir de dados processados.")
    parser.add_argument("input_file", type=Path, help="Caminho para o arquivo CSV processado (responses_clean.csv).")
    parser.add_argument("-o", "--output_dir", type=Path, default=Path("reports/figs"),
                        help="Diretório onde os gráficos serão salvos.")
    args = parser.parse_args()

    try:
        create_visualizations(args.input_file, args.output_dir)
        logging.info("Todas as visualizações foram geradas com sucesso!")
        return 0
    except Exception:
        logging.critical("A geração de visualizações falhou. Verifique os logs de erro.")
        return 1

if __name__ == "__main__":
    sys.exit(main())