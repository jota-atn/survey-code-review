import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from src.analysis import (
    calculate_descriptive_stats,
    calculate_correlations,
    analyze_data
)

def test_calculate_descriptive_stats():
    dados_teste = pd.DataFrame({'nota': [1, 2, 3, 4, 5], 'id': [101, 102, 103, 104, 105]}) 
    resultados = calculate_descriptive_stats(dados_teste)
    
    assert len(resultados) == 3

    assert any("nota**: Média=3.00, Desvio Padrão=1.58" in s for s in resultados)
    assert any("id**: Média=103.00, Desvio Padrão=1.58" in s for s in resultados)

def test_calculate_correlations_sucesso():
    dados_teste = pd.DataFrame({
        'empatia': [1, 2, 3, 4, 5],
        'ajuda_aprendizado': [1, 2, 3, 4, 5]
    })
    pares_teste = [("empatia", "ajuda_aprendizado")]
    
    resultados = calculate_correlations(dados_teste, pares_teste)

    assert len(resultados) == 2
    assert "Coeficiente (r)=1.000" in resultados[1]
    assert "Estatisticamente Significante" in resultados[1]

def test_calculate_correlations_dados_insuficientes():
    dados_teste = pd.DataFrame({
        'respira': [1, np.nan, 3, np.nan],
        'contribui_relacionamento': [5, 4, np.nan, 2]
    })
    pares_teste = [("respira", "contribui_relacionamento")]

    resultados = calculate_correlations(dados_teste, pares_teste)

    assert "Não foi possível calcular" in resultados[1]

def test_analyze_data_cria_relatorio_corretamente(tmp_path):
    arquivo_entrada = tmp_path / "clean_data.csv"
    arquivo_saida = tmp_path / "report.md"
    
    dados_teste = pd.DataFrame({
        'empatia': [1, 2, 3, 4, 5],
        'ajuda_aprendizado': [5, 4, 3, 2, 1]
    })
    dados_teste.to_csv(arquivo_entrada, index=False)
    
    analyze_data(input_path=arquivo_entrada, output_path=arquivo_saida)
    
    assert arquivo_saida.exists()
    
    conteudo_relatorio = arquivo_saida.read_text(encoding='utf-8')
    
    assert "# Relatório de Análise de Dados" in conteudo_relatorio
    assert "## Estatísticas Descritivas" in conteudo_relatorio
    assert "empatia**: Média=3.00, Desvio Padrão=1.58" in conteudo_relatorio
    assert "## Análise de Correlação (Spearman)" in conteudo_relatorio
    assert "empatia ↔ ajuda_aprendizado**: Coeficiente (r)=-1.000" in conteudo_relatorio