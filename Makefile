.PHONY: test

test:
	pytest --isort --black --mypy
