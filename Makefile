.PHONY: test

test:
	pytest --isort --flake8 --black
