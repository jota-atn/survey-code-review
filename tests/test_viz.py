import pytest
import pandas as pd
from pathlib import Path

from src.viz import create_visualizations

def test_create_visualizations_sucesso(tmp_path):
    input_file = tmp_path / "clean_data.csv"
    output_dir = tmp_path / "test_figs"

    test_data = pd.DataFrame({
        'empatia': [1, 5, 3, 4],
        'respira': [5, 2, 4, 3],
        'vinculo': ['Aluno', 'Professor', 'Aluno', 'Aluno']
    })
    test_data.to_csv(input_file, index=False)

    create_visualizations(input_path=input_file, output_dir=output_dir)
    
    assert output_dir.is_dir(), "O diretório de saída não foi criado."
    
    expected_files = [
        "empatia_bar_chart.png",
        "respira_bar_chart.png",
        "correlation_heatmap.png"
    ]
    for filename in expected_files:
        assert (output_dir / filename).exists(), f"Arquivo esperado '{filename}' não foi encontrado."

def test_create_visualizations_sem_dados_suficientes_para_heatmap(tmp_path):
    input_file = tmp_path / "clean_data_single_numeric.csv"
    output_dir = tmp_path / "test_figs_single"

    test_data = pd.DataFrame({
        'empatia': [1, 5, 3, 4],
        'vinculo': ['Aluno', 'Professor', 'Aluno', 'Aluno']
    })
    test_data.to_csv(input_file, index=False)

    create_visualizations(input_path=input_file, output_dir=output_dir)

    assert output_dir.is_dir()

    assert (output_dir / "empatia_bar_chart.png").exists()

    assert not (output_dir / "correlation_heatmap.png").exists()