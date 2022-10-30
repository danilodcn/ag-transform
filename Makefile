.PHONE: format, clear, test, lint

default: test

clear:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

test:
	@echo "Testing ..."
	poetry run python manager.py tests

format:
	@echo "formating the project"
	isort .
	black .
	make lint

lint:
	poetry run flake8 tcc/core  --count --show-source --statistics

mypy:
	mypy .
