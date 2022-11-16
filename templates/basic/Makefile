# =============================================================================
.SILENT:
.DEFAULT_GOAL:=run
SHELL:=/usr/bin/bash

PROJECT_NAME:=project
VENV_DIR:=.venv
ACTIVATE:=source .venv/bin/activate &&

.PHONY: setup run lint format test build

setup:
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	poetry install

run:
	python $(PROJECT_NAME)

lint:
	flake8 --show-source .
	bandit -q -r -c "pyproject.toml" .

format:
	black .

test:
	pytest

build:
	poetry build -q

clean:
	rm -rf $(VENV_DIR)
	find . -type d -name '__pycache__' -exec rm -rf {} +
# =============================================================================
