env:
	uv venv
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check . --fix

format:
	uv run ruff format .

run:
	uv run uvicorn patient_name_extractor.main:app --host 0.0.0.0 --port 8080

uv-export-requirements:
	uv export --format requirements-txt > requirements.txt
