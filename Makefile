.PHONY: format run all

format:
	black src
	isort src
run:
	python src/main.py

all: format run

