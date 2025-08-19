import pytest
import pandas as pd
import numpy as np 
from pathlib import Path

from src.clean import aplicar_mapeamento_colunas, clean_data, RENAME_MAP

def test_aplicar_mapeamento_colunas_sucesso():
    dados_iniciais = pd.DataFrame({'pergunta': ['Sempre', 'Nunca']})
    mapeamento = {'Nunca': 1, 'Sempre': 5}
    
    df_resultante = aplicar_mapeamento_colunas(dados_iniciais, ['pergunta'], mapeamento)
    
    assert df_resultante['pergunta'].tolist() == [5, 1]

def test_aplicar_mapeamento_colunas_com_coluna_inexistente():
    dados_iniciais = pd.DataFrame({'coluna_real': ['Sempre', 'Nunca']})
    mapeamento = {'Nunca': 1, 'Sempre': 5}
    
    df_resultante = aplicar_mapeamento_colunas(dados_iniciais, ['coluna_inexistente'], mapeamento)
    
    pd.testing.assert_frame_equal(df_resultante, dados_iniciais)

def test_aplicar_mapeamento_colunas_sem_colunas_alvo():
    dados_iniciais = pd.DataFrame({'pergunta': ['Sempre', 'Nunca']})
    mapeamento = {'Nunca': 1, 'Sempre': 5}
    
    df_resultante = aplicar_mapeamento_colunas(dados_iniciais, [], mapeamento)
    
    pd.testing.assert_frame_equal(df_resultante, dados_iniciais)


def test_clean_data_pipeline_completo(tmp_path):
    arquivo_entrada = tmp_path / "raw_data.csv"
    arquivo_saida = tmp_path / "clean_data.csv"
    
    coluna_vinculo_original = "Qual seu vínculo com o curso de Computação da UFCG?"
    coluna_empatia_original = "Você costuma considerar que o outro pode estar aprendendo ou inseguro antes de criticar um código?"

    dados_teste_brutos = pd.DataFrame({
        coluna_vinculo_original: ["Aluno", "Professor", np.nan, "Aluno"],
        coluna_empatia_original: ["Sempre", "Às vezes", "Nunca", "Sempre"], # A última linha é duplicata da primeira
        "outra_coluna": [1, 2, 3, 1]
    })
    dados_teste_brutos.to_csv(arquivo_entrada, index=False)
    
    clean_data(caminho_entrada=arquivo_entrada, caminho_saida=arquivo_saida)

    assert arquivo_saida.exists(), "O arquivo de saída não foi criado."
    
    df_resultado = pd.read_csv(arquivo_saida)

    dados_esperados = pd.DataFrame({
        'vinculo': ["Aluno", "Professor"],
        'empatia': [5, 3],
        'outra_coluna': [1, 2]
    })

    pd.testing.assert_frame_equal(df_resultado, dados_esperados)