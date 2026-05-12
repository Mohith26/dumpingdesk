# DumpingDesk

MVP vertical slice for automating U.S. Department of Commerce ADD questionnaire response work.

This repository starts with a deliberately narrow path:

- Flat-file ingestion for CSV/XLSX sales and cost data
- Canonical transaction records for U.S. sales, home-market sales, and costs
- Validation events for missing fields, date range issues, cost coverage, and price anomalies
- Decimal-based AD margin calculation foundations
- A Next.js review shell for matter status, validation events, calculations, and drafts
- Local developer tooling for API tests, web linting/builds, and CI

## Repository Layout

```text
apps/web/        Next.js App Router frontend
services/api/    FastAPI backend and domain logic
docs/            Architecture notes and implementation plan
.github/         CI workflows
```

## Quick Start

```bash
# Backend
cd services/api
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
uvicorn dumpingdesk_api.main:app --reload

# Frontend
cd ../../apps/web
npm install
npm run dev
```

The frontend expects the API at `http://localhost:8000` unless `NEXT_PUBLIC_API_BASE_URL` is set.
