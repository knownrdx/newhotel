# Hotel WiFi Management SaaS for MikroTik RouterOS

A multi-tenant SaaS starter for hotels to automate guest WiFi provisioning, captive portal access, voucher generation, router management, and guest analytics.

## Quick start with Docker Compose

```bash
docker compose up --build -d
docker compose logs -f seed
```

Open:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Health check: `http://localhost:8000/health`
- Guest portal: `http://localhost:3000/portal?hotel=demo-hotel`
- Admin dashboard: `http://localhost:3000/admin`

## Demo credentials

- Admin login: `admin@demo.local` / `admin123`
- Guest login by room: `101` + `Park`
- Guest login by voucher: `DEMO101`

## Files for Docker

- `compose.yaml` → main Docker Compose file
- `docker-compose.yml` → duplicate for compatibility
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `.env.example`

## Run commands

```bash
docker compose up --build -d
docker compose ps
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f worker
docker compose down
```

## What this stack includes

- PostgreSQL 16
- Redis 7
- FastAPI backend
- PMS polling worker
- Next.js frontend
- Demo data seeder

## Notes

This project is now packaged to run directly with Docker Compose. For real hotel deployment, update the environment values, PMS mapping, hotel branding, and MikroTik router credentials.
