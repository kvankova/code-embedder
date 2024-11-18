.PHONY: build run

build:
	docker build -t code-embedder .

run:
	make build
	docker run --rm -it code-embedder

test:
	poetry run pytest
