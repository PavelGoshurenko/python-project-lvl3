# Makefile

install:
	poetry install
lint:
	poetry run flake8 page_loader
test:
	poetry run pytest


