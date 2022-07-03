.PHONE: tests, format

tests:
	@echo "Testing ..."
	poetry run python manager.py tests


format:
	@echo "formating the project"
	isort .
	black .

lint:
	flake8 tcc/core
