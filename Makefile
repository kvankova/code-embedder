.PHONY: build run

build:
	docker build -t code-embedder .

run:
	make build
	docker run --rm -it --env-file=.env code-embedder

test:
	poetry run pytest

del:
	gh release delete 0.0.1
	git push origin --delete 0.0.1
	git tag -d 0.0.1
	gh release create 0.0.1 --target add_typer -t "Testing"
