.PHONY: install test lint format type-check clean

install:
	pip install -r requirements.txt
	pip install -e .

test:
	pytest tests/ --cov=calendar --cov-report=term-missing

lint:
	flake8 calendar/ tests/
	black --check calendar/ tests/

format:
	black calendar/ tests/

type-check:
	mypy calendar/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 