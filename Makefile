.PHONE: tests, format

tests:
	@echo "Testing ..."
	poetry run python manage.py tests


format:
	@echo "formating the project"
	isort .
	black .
