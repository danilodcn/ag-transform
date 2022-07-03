.PHONE: tests, format

clear:
	find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

tests:
	@echo "Testing ..."
	poetry run python manager.py tests


format:
	@echo "formating the project"
	isort .
	black .

lint:
	flake8 tcc/core
