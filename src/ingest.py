import argparse
import logging
import sys
import pandas as pd
from pathlib import Path
from typing import List

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ingest_data(caminho_entrada: Path, caminho_saida: Path, engine: str = 'c') -> None:
    logging.info(f"Iniciando a ingestão do arquivo: {caminho_entrada}")
    
    if not caminho_entrada.exists():
        logging.error(f"Arquivo de entrada não encontrado em: {caminho_entrada}")
        raise FileNotFoundError(f"Arquivo de entrada não encontrado em: {caminho_entrada}")

    try:
        responses_df = pd.read_csv(caminho_entrada, engine=engine)
        logging.info(f"Arquivo lido com sucesso. Encontradas {responses_df.shape[0]} linhas e {responses_df.shape[1]} colunas.")

        caminho_saida.parent.mkdir(parents=True, exist_ok=True)
        logging.info(f"Garantindo que o diretório de saída exista: {caminho_saida.parent}")

        responses_df.to_csv(caminho_saida, index=False)
        logging.info(f"Dados salvos com sucesso em: {caminho_saida}")

    except pd.errors.EmptyDataError as e:
        logging.error("O arquivo de entrada está vazio ou mal formatado.")
        raise e
    except pd.errors.ParserError as e:
        logging.error("Erro ao fazer o parse do arquivo CSV. Verifique o formato.")
        raise e
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado durante a ingestão: {e}")
        raise e


def main(argv: List[str] = None) -> int:
    parser = argparse.ArgumentParser(description="Script de ingestão de dados de um arquivo CSV.")
    parser.add_argument("input_file", type=Path, help="Caminho para o arquivo CSV de entrada (exportado do Forms).")
    parser.add_argument("-o", "--output_file", type=Path, default=Path("data/raw/responses.csv"),
                        help="Caminho para o arquivo CSV de saída. Padrão: data/raw/responses.csv")

    args = parser.parse_args(argv)

    try:
        ingest_data(args.input_file, args.output_file)
        logging.info("INGESTÃO CONCLUÍDA COM SUCESSO!")
        return 0 
    except (FileNotFoundError, pd.errors.EmptyDataError, pd.errors.ParserError) as e:
        return 1 
    except Exception as e:
        logging.critical(f"Uma falha crítica impediu a execução: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())