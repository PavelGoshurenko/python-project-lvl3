# Makefile

install:
	poetry install
lint:
	poetry run flake8 page_loader
test:
	poetry run pytest --cov=page_loader --cov-report xml tests/
publish:
	poetry build
	poetry publish -r testpypi


