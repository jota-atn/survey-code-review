RAW_DIR         := data/raw
PROCESSED_DIR   := data/processed
REPORTS_DIR     := reports
SRC_DIR         := src

ARQ_INICIAL     ?= "data/raw/forms_export.csv"
RAW_FILE        := $(RAW_DIR)/responses.csv
PROC_FILE       := $(PROCESSED_DIR)/responses_clean.csv
ANALYSIS_FILE   := $(REPORTS_DIR)/analysis_summary.txt
VIZ_DIR         := $(REPORTS_DIR)/figs

VENV            := venv
PYTHON          := $(VENV)/bin/python
PIP             := $(VENV)/bin/pip

.PHONY: all setup ingest clean_data analyze viz dash reset

all: $(VIZ_DIR)

ingest: $(RAW_FILE)

$(RAW_FILE): $(SRC_DIR)/ingest.py
	@echo "--- Executando a ingestão de dados ---"
	$(PYTHON) $(SRC_DIR)/ingest.py $(ARQ_INICIAL)

clean_data: $(PROC_FILE)

$(PROC_FILE): $(RAW_FILE) $(SRC_DIR)/clean.py
	@echo "--- Executando a limpeza dos dados ---"
	$(PYTHON) $(SRC_DIR)/clean.py $(RAW_FILE) -o $(PROC_FILE)

analyze: $(ANALYSIS_FILE)

$(ANALYSIS_FILE): $(PROC_FILE) $(SRC_DIR)/analysis.py
	@echo "--- Executando a análise ---"
	$(PYTHON) $(SRC_DIR)/analysis.py $(PROC_FILE) > $(ANALYSIS_FILE)

viz: $(VIZ_DIR)

$(VIZ_DIR): $(PROC_FILE) $(SRC_DIR)/viz.py
	@echo "--- Gerando visualizações ---"
	$(PYTHON) $(SRC_DIR)/viz.py $(PROC_FILE)

.ONESHELL:

setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

dash:
	streamlit run $(SRC_DIR)/app_streamlit.py

reset:
	@echo "--- Limpando arquivos gerados ---"
	rm -rf __pycache__ */__pycache__ .pytest_cache
	rm -rf $(PROCESSED_DIR)/*.* $(RAW_DIR)/*.* $(REPORTS_DIR)/*.*

test:
	@echo "--- Testando..."
	$(PYTHON) -m pytest -v