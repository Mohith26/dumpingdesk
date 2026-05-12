.PHONY: test lint api web

test:
	cd services/api && python -m pytest

lint:
	cd services/api && ruff check .
	cd apps/web && npm run lint

api:
	cd services/api && uvicorn dumpingdesk_api.main:app --reload

web:
	cd apps/web && npm run dev
