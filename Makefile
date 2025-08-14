RAW_DIR := data/raw
PROCESSED_DIR := data/processed 
SRC_DIR := src

RAW_FILE := $(RAW_DIR)/responses.csv
PROC_FILE := $(PROC_DIR)/responses_clean.csv

VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.ONESHELL:

setup:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

ingest:
	$(PYTHON) $(SRC_DIR)/ingest.py $(ARQ)

clean:
	$(PYTHON) $(SRC_DIR)/clean.py

analyze:
	$(PYTHON) $(SRC_DIR)/analysis.py

viz:
	$(PYTHON) $(SRC_DIR)/viz.py

dash:
	streamlit run $(SRC_DIR)/app_streamlit.py

reset:
	rm -rf __pycache__ */__pycache__ .pytest_cache
	rm -rf $(PROC_DIR)/*.csv
	rm -rf reports/figs/*.png

all: ingest clean analyze viz