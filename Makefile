.PHONY: install test lint data validate demo demo-clickhouse up down

install:
	pip install -e .[dev]

test:
	pytest -m "not integration" --cov=dq tests/

lint:
	ruff check .

data:
	python fixtures/generate_data.py --mode clean
	python fixtures/generate_data.py --mode corrupt

validate:
	dq validate checks/

demo:
	dq demo --backend duckdb

demo-clickhouse:
	dq demo --backend clickhouse

up:
	docker-compose up -d

down:
	docker-compose down
