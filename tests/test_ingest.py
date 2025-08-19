import pytest
import pandas as pd
from pathlib import Path

from src.ingest import ingest_data

def test_ingest_data_sucesso(tmp_path):
    arquivo_entrada = tmp_path / "input.csv"
    arquivo_saida = tmp_path / "output.csv"
    dados_iniciais = pd.DataFrame({'coluna1': [1, 2], 'coluna2': ['A', 'B']})
    dados_iniciais.to_csv(arquivo_entrada, index=False)
    
    ingest_data(caminho_entrada=arquivo_entrada, caminho_saida=arquivo_saida)
    
    assert arquivo_saida.exists(), "O arquivo de saída não foi criado."
    df_saida = pd.read_csv(arquivo_saida)
    pd.testing.assert_frame_equal(df_saida, dados_iniciais)

def test_ingest_data_arquivo_nao_encontrado(tmp_path):
    arquivo_entrada = tmp_path / "arquivo_que_nao_existe.csv"
    arquivo_saida = tmp_path / "output.csv"
    
    with pytest.raises(FileNotFoundError):
        ingest_data(caminho_entrada=arquivo_entrada, caminho_saida=arquivo_saida)

def test_ingest_data_csv_vazio(tmp_path):
    arquivo_entrada = tmp_path / "vazio.csv"
    arquivo_entrada.touch()
    arquivo_saida = tmp_path / "output.csv"
    
    with pytest.raises(pd.errors.EmptyDataError):
        ingest_data(caminho_entrada=arquivo_entrada, caminho_saida=arquivo_saida)

def test_ingest_data_csv_malformado(tmp_path):
    arquivo_entrada = tmp_path / "malformado.csv"
    arquivo_entrada.write_text('"header1","header2"\n"dado1,"dado2"')
    arquivo_saida = tmp_path / "output.csv"
    
    with pytest.raises(pd.errors.ParserError):
        ingest_data(caminho_entrada=arquivo_entrada, caminho_saida=arquivo_saida, engine='python')