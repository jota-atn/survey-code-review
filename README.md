# Pesquisa sobre Inteligência Emocional no Code Review

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9B53?style=for-the-badge&logo=pytest&logoColor=white)
![Make](https://img.shields.io/badge/GNU%20Make-4DB6AC?style=for-the-badge&logo=gnu-make&logoColor=white)

## Descrição
Este projeto tem como objetivo coletar, processar e analisar respostas de um formulário sobre inteligência emocional aplicada ao processo de *code review* entre estudantes e membros do curso de Ciência da Computação da UFCG.  
A implementação foi desenvolvida para permitir a ingestão de dados exportados do Google Forms, limpeza e padronização das respostas, geração de estatísticas descritivas, análise de correlações, visualizações gráficas e um dashboard interativo para exploração dos resultados, consistindo em um pipeline de dados automatizado e testável que realiza todas essas operações.


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
├── venv/                 # Ambiente virtual (ignorado pelo Git)
├── Makefile              # Orquestrador de automação do pipeline
├── pytest.ini            # Configuração do Pytest
├── requirements.txt      # Dependências do projeto
├── .gitignore
└── README.md
```

## Instalação

Certifique-se de ter o Makefile devidamente instalado em sua máquina.

Para configurar o projeto localmente, siga os passos abaixo.

### 1. Clonar o Repositório
```bash
git clone https://github.com/jota-atn/survey-code-review.git
cd survey-code-review
```

### 2. Configurar o ambiente:
Este projeto usa um Makefile para automatizar a configuração. O comando abaixo irá criar o ambiente virtual e instalar todas as dependências necessárias.
```bash
make setup
```


## Uso
Todas as etapas do projeto podem ser executadas através de comandos make simples e padronizados, seguindo, ou não, um pipeline automatizado.

### Executar o Pipeline Completo
Para rodar todas as etapas, da ingestão dos dados brutos até a geração das visualizações, execute:

```bash
# Certifique-se de que seu arquivo de dados brutos está no local
# configurado no Makefile (padrão: "data/raw/forms_export.csv")
make all
```
Você também pode especificar o arquivo de entrada ao rodar a ingestão pela primeira vez:

```bash
make ingest ARQ_INICIAL="caminho/do/seu/arquivo.csv"
```

### Executar os Testes
Para garantir que todo o pipeline está funcionando corretamente, rode a suíte de testes completa:

```bash
make test
```

### Visualizar o Dashboard Interativo
Para explorar os dados de forma interativa, inicie o dashboard com Streamlit:

```bash
make dash
```

### Limpar os Arquivos Gerados
Para apagar todos os arquivos gerados (/data/processed, /reports, etc.) e recomeçar, use:

```bash
make reset
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
