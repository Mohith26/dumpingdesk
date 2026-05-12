# Railway Deployment

Railway should deploy this repository as either:

1. A quick root deployment for the demo web app, or
2. Two isolated services for the full MVP shape.

## Quick Test Deployment

Deploy the repository root. The root `Dockerfile` and `railway.toml` build and start `apps/web`.

This is enough to click through the dashboard because the frontend has fallback demo data when the API is not available.

## Full Two-Service Deployment

Create two Railway services from the same GitHub repository.

### Web Service

- Root directory: `/apps/web`
- Config file: `/apps/web/railway.toml`
- Environment:
  - `NEXT_PUBLIC_API_BASE_URL=<api service public URL>`

### API Service

- Root directory: `/services/api`
- Config file: `/services/api/railway.toml`
- Healthcheck: `/health`

The API currently uses in-memory sample data, so Postgres and Redis are not required for the demo endpoints yet.
