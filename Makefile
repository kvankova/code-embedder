.PHONY: build
curr_dir = $(shell pwd)

build:
	docker build -t code-embedder .

run:
	make build
	docker run --rm -it --env-file=.env code-embedder 
	