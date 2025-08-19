import pytest
import pandas as pd
from pathlib import Path

from src.app_streamlit import load_data, filter_data

def test_load_data_sucesso(tmp_path):
    file_path = tmp_path / "test_data.csv"
    expected_df = pd.DataFrame({'col1': [1, 2]})
    expected_df.to_csv(file_path, index=False)

    loaded_df = load_data(file_path)

    pd.testing.assert_frame_equal(loaded_df, expected_df)

def test_filter_data():
    test_data = pd.DataFrame({
        'vinculo': ['Aluno', 'Ex-aluno', 'Professor', 'Aluno'],
        'participou_role': ['Autor', 'Revisor', 'Revisor', 'Autor'],
        'idade': [20, 30, 40, 22]
    })
    
    result1 = filter_data(test_data, 
                          vinculos_selecionados=['Aluno'], 
                          papeis_selecionados=['Autor'])

    result2 = filter_data(test_data, 
                          vinculos_selecionados=['Aluno', 'Ex-aluno', 'Professor'], 
                          papeis_selecionados=['Revisor'])

    result3 = filter_data(test_data, 
                          vinculos_selecionados=['Professor'], 
                          papeis_selecionados=['Autor'])

    assert len(result1) == 2
    assert result1['vinculo'].unique() == ['Aluno']
    assert result1['participou_role'].unique() == ['Autor']

    assert len(result2) == 2
    assert 'Ex-aluno' in result2['vinculo'].values
    assert 'Professor' in result2['vinculo'].values
    
    assert result3.empty