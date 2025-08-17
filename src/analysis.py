import argparse
import logging
import sys
import pandas as pd
from pathlib import Path
from scipy.stats import spearmanr

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

CORRELATION_PAIRS = [
    ("empatia", "ajuda_aprendizado"),
    ("respira", "contribui_relacionamento"),
    ("feedback_influencia_clima", "influencia_motivacao")
]

def calculate_descriptive_stats(responses_clean_df):
    results = ["## Estatísticas Descritivas\n"]
    numeric_cols = responses_clean_df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_cols:
        mean = responses_clean_df[col].mean()
        std = responses_clean_df[col].std()
        results.append(f"- **{col}**: Média={mean:.2f}, Desvio Padrão={std:.2f}")
    return results

def calculate_correlations(responses_clean_df, pairs):
    results = ["\n## Análise de Correlação (Spearman)\n"]
    for x, y in pairs:
        if x in responses_clean_df.columns and y in responses_clean_df.columns:
            clean_responses_clean_df = responses_clean_df[[x, y]].dropna()
            if len(clean_responses_clean_df) > 1:
                r, p = spearmanr(clean_responses_clean_df[x], clean_responses_clean_df[y])
                significance = "Estatisticamente Significante" if p < 0.05 else "Não Significante"
                results.append(f"- **{x} ↔ {y}**: Coeficiente (r)={r:.3f}, p-valor={p:.4f} (*{significance}*)")
            else:
                results.append(f"- **{x} ↔ {y}**: Não foi possível calcular (dados insuficientes após remover nulos).")
    return results

def analyze_data(input_path, output_path):
    logging.info(f"Iniciando análise do arquivo: {input_path}")

    if not input_path.exists():
        logging.error(f"Arquivo de entrada não encontrado: {input_path}")
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_path}")

    try:
        responses_clean_df = pd.read_csv(input_path)
        logging.info(f"Arquivo lido com sucesso ({responses_clean_df.shape[0]} linhas, {responses_clean_df.shape[1]} colunas).")

        report_content = ["# Relatório de Análise de Dados\n"]
        report_content.extend(calculate_descriptive_stats(responses_clean_df))
        report_content.extend(calculate_correlations(responses_clean_df, CORRELATION_PAIRS))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_content))
        
        logging.info(f"Relatório de análise salvo com sucesso em: {output_path}")

    except pd.errors.EmptyDataError:
        logging.error(f"O arquivo de entrada está vazio: {input_path}")
        raise
    except Exception as e:
        logging.error(f"Um erro inesperado ocorreu durante a análise: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Gera um relatório de análise a partir de dados processados.")
    parser.add_argument("input_file", type=Path, help="Caminho para o arquivo CSV processado (responses_clean.csv).")
    parser.add_argument("-o", "--output_file", type=Path, default=Path("reports/analysis_summary.md"),
                        help="Caminho para salvar o relatório de saída (em formato Markdown).")
    args = parser.parse_args()

    try:
        analyze_data(args.input_file, args.output_file)
        logging.info("Análise concluída com sucesso!")
        return 0
    except Exception:
        logging.critical("A análise falhou. Verifique os logs de erro acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())