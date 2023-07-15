clear:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -path "*.egg-info*" -delete
	find . -type d -path "*.egg-info" -delete
	find . -type f -path "*.egg-info*" -delete
	find . -type d -path "*.egg-info" -delete
	find . -type f -name "*.sqlite3_*" -delete
	rm -f ./.coverage
	rm -r htmlcov dist .pytest_cache
