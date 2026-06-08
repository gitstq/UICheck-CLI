.PHONY: help install test lint run clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-12s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in development mode
	pip install -e .

test: ## Run tests
	python -m pytest tests/ -v

lint: ## Run lint checks
	python -m py_compile uicheck_cli/*.py
	python -m py_compile uicheck_cli/rules/*.py

run: ## Run CLI with sample input
	python -m uicheck_cli --help

scan: ## Scan current directory
	python -m uicheck_cli scan . --verbose

rules: ## List all rules
	python -m uicheck_cli rules list --verbose

clean: ## Clean build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name *.egg-info -exec rm -rf {} + 2>/dev/null || true
	rm -f uicheck-report.json uicheck-report.md
