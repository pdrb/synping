lint:
	ruff check
	ruff format

test:
	python3 -m unittest -v
