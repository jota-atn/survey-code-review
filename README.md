# Pesquisa sobre Inteligência Emocional no Code Review

## Descrição
Este projeto tem como objetivo coletar, processar e analisar respostas de um formulário sobre inteligência emocional aplicada ao processo de *code review* entre estudantes e membros do curso de Ciência da Computação da UFCG.  
A implementação foi desenvolvida para permitir a ingestão de dados exportados do Google Forms, limpeza e padronização das respostas, geração de estatísticas descritivas, análise de correlações, visualizações gráficas e um dashboard interativo para exploração dos resultados.

## Estrutura do Projeto
```
survey-code-review/
├─ data/
│  ├─ raw/               # Dados brutos exportados do Google Forms
│  └─ processed/         # Dados processados e prontos para análise
├─ reports/
│  └─ figs/              # Gráficos gerados pelos scripts de visualização
├─ src/
│  ├─ ingest.py          # Ingestão dos dados brutos
│  ├─ clean.py           # Limpeza e padronização das respostas
│  ├─ analysis.py        # Estatísticas descritivas e correlações
│  ├─ viz.py             # Geração de gráficos e heatmaps
│  └─ app_streamlit.py   # Dashboard interativo com Streamlit
├─ tests/                # Testes automatizados
├─ requirements.txt      # Dependências do projeto
└─ README.md             # Documentação do projeto
```

## Instalação
1. Clone este repositório:
```bash
git clone <url-do-repositorio>
cd survey-code-review
```
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso
1. Coloque o arquivo CSV exportado do Google Forms na pasta `data/raw/` ou utilize o script de ingestão:
```bash
python src/ingest.py caminho/do/arquivo.csv
```
2. Limpe e padronize os dados:
```bash
python src/clean.py
```
3. Gere estatísticas e correlações:
```bash
python src/analysis.py
```
4. Crie visualizações:
```bash
python src/viz.py
```
5. Abra o dashboard interativo:
```bash
streamlit run src/app_streamlit.py
```

## Estrutura dos Dados
O formulário é composto por questões de múltipla escolha e escalas de Likert (1 a 5), mapeadas para valores numéricos.  
As colunas incluem informações sobre:
- **Perfil**: vínculo com o curso e experiência prévia em code reviews.
- **Experiência com Code Review**: frequência, treinamento, papel no processo.
- **Clima e Comunicação**: percepção de respeito, clareza e eventuais conflitos.
- **Inteligência Emocional**: empatia, autocontrole e comunicação não-violenta.
- **Impacto no Aprendizado e Motivação**: benefícios percebidos e relação com o clima da equipe.

## Licença
Este projeto é de uso acadêmico e não possui licença pública definida.