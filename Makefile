DIRECTORY := src

.PHONY: help
help:  ## Show this help
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: setup-dev
setup-dev:  ## Prepare dev env (install requirements)
	pip install -r requirements.dev.txt

.PHONY: init-db
init-db:  ## Create tables and fill with initial data
	docker-compose exec api python init_db.py

.PHONY: start-dev
start-dev:  ## Start dev services
	docker-compose up -d --build

.PHONY: stop-dev
stop-dev:  ## Stop dev services
	docker-compose stop

.PHONY: build
build:  ## Build dev services
	docker-compose build

.PHONY: test
test:  ## Run unit tests
	pytest

.PHONY: lint
lint:  ## Run linters (mypy, pylint, black, isort)
	mypy $(DIRECTORY)
	pylint $(DIRECTORY)
	black -l 100 --check $(DIRECTORY)
	isort --check-only -rc $(DIRECTORY)

.PHONY: format
format:  ## Reformat code (black, isort)
	black -l 100 $(DIRECTORY)
	isort -rc $(DIRECTORY)
