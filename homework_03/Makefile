.PHONY: build run

build:
	@echo "--- Building Image ---"
	docker build -t homework_03:latest .

run: build
	@echo "--- Starting Container ---"
	docker run -p 8000:8000 --rm -d homework_03:latest

rm_inactive:
	docker rm $$(docker ps -aq)