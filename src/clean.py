import argparse
import logging
import sys
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RENAME_MAP = {
    "Você está atualmente matriculado no curso de Ciência da Computação na UFCG?":"matriculado",
    "Qual seu vínculo com o curso de Computação da UFCG?":"vinculo",
    "Você já participou de Code Reviews durante sua graduação?":"participou_role",
    "Com que frequência você participa de Code Reviews?":"freq_participa",
    "Você recebeu orientações ou treinamentos formais sobre como realizar Code Reviews?":"treinamento",
    "Já se sentiu desconfortável ou atacado(a) durante um Code Review?":"desconforto",
    "Você já presenciou comentários ríspidos ou mal interpretados em Code Reviews?":"comentarios_rispidos",
    "Você acredita que o jeito de dar feedback influencia diretamente no clima da equipe?":"feedback_influencia_clima",
    "Você já evitou revisar ou enviar código por medo de críticas negativas?":"evitou_por_medo",
    "Antes de responder um comentário que não gostou, você costuma “respirar fundo” ou pensar antes de responder?":"respira",
    "Você costuma considerar que o outro pode estar aprendendo ou inseguro antes de criticar um código?":"empatia",
    "Nos Code Reviews que você participa, a comunicação geralmente é clara e respeitosa?":"comunicacao_respeitosa",
    "Você já fez um comentário técnico que foi interpretado como pessoal, mesmo sem essa intenção?":"comentario_malinterpre",
    "Você já recebeu um feedback que te motivou a melhorar significativamente seu código?":"feedback_motivador",
    "Você sente que Code Reviews ajudam a melhorar suas habilidades de programação?":"ajuda_aprendizado",
    "Você sente que Code Reviews contribuem para um bom relacionamento dentro da equipe?":"contribui_relacionamento",
    "Você considera que a forma como o feedback é dado influencia sua motivação para contribuir no projeto?":"influencia_motivacao"
}

LIKERT_FREQUENCIA = {
    'Nunca':1, 'Raramente':2, 'Às vezes':3, 'Frequentemente':4, 'Sempre':5
}
LIKERT_ACORDO = {
    'Discordo totalmente':1, 'Discordo':2, 'Neutro':3, 'Concordo':4, 'Concordo totalmente':5
}

FREQ_COLS = [
    'freq_participa','desconforto','comentarios_rispidos','evitou_por_medo',
    'respira','empatia','comunicacao_respeitosa','comentario_malinterpre','feedback_motivador'
]
ACORDO_COLS = [
    'feedback_influencia_clima','ajuda_aprendizado','contribui_relacionamento','influencia_motivacao'
]

def aplicar_mapeamento_colunas(df, colunas_alvo, mapeamento):
    df_copy = df.copy()
    colunas_existentes = [col for col in colunas_alvo if col in df_copy.columns]
    
    logging.info(f"Aplicando mapeamento em {len(colunas_existentes)} colunas-alvo.")
    for col in colunas_existentes:
        df_copy[col] = df_copy[col].map(mapeamento)
        
    return df_copy

def clean_data(caminho_entrada, caminho_saida):
    logging.info(f"Iniciando a limpeza e normatização do arquivo: {caminho_entrada}")    

    if not caminho_entrada.exists():
        logging.error(f"Arquivo de entrada não encontrado em: {caminho_entrada}")
        raise FileNotFoundError(f"Arquivo de entrada não encontrado em: {caminho_entrada}")

    try:
        df = pd.read_csv(caminho_entrada)
        logging.info(f"Arquivo lido com sucesso. Encontradas {df.shape[0]} linhas e {df.shape[1]} colunas.")

        df = df.rename(columns=RENAME_MAP)
        logging.info("Colunas renomeadas com sucesso.")
        
        linhas_antes = df.shape[0]
        df = df[df['vinculo'].notna()]
        linhas_removidas = linhas_antes - df.shape[0]
        logging.info(f"Removidas {linhas_removidas} linhas com a coluna 'vinculo' vazia.")

        df = aplicar_mapeamento_colunas(df, FREQ_COLS, LIKERT_FREQUENCIA)
        df = aplicar_mapeamento_colunas(df, ACORDO_COLS, LIKERT_ACORDO)
        
        linhas_antes = df.shape[0]
        df = df.drop_duplicates()
        duplicatas_removidas = linhas_antes - df.shape[0]
        logging.info(f"Removidas {duplicatas_removidas} linhas duplicadas.")

        caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(caminho_saida, index=False)
        logging.info(f"Arquivo processado salvo em: {caminho_saida} ({df.shape[0]} linhas finais)")

    except pd.errors.EmptyDataError as e:
        logging.error("O arquivo de entrada está vazio ou mal formatado.")
        raise e
    except pd.errors.ParserError as e:
        logging.error("Erro ao fazer o parse do arquivo CSV. Verifique o formato.")
        raise e
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado durante a limpeza: {e}")
        raise e
    
def main(argv=None):
    parser = argparse.ArgumentParser(description="Script de limpeza e normatização de dados de um arquivo CSV.")
    parser.add_argument("input_file", type=Path, help="Caminho para o arquivo CSV de entrada (gerado pelo ingest.py).")
    parser.add_argument("-o", "--output_file", type=Path, default=Path("data/processed/responses_clean.csv"),
                        help="Caminho para o arquivo CSV de saída. Padrão: data/processed/responses_clean.csv")

    args = parser.parse_args(argv)

    try:
        clean_data(args.input_file, args.output_file)
        logging.info("PROCESSO DE LIMPEZA CONCLUÍDO COM SUCESSO!")
        return 0 
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError):
        logging.error("A execução falhou devido a um erro de arquivo ou de parsing.")
        return 1 
    except Exception as e:
        logging.critical(f"Uma falha crítica impediu a execução: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())