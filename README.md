# Hotel WiFi SaaS - Coolify Ready

This package is prepared for **Coolify Docker Compose Empty** deployment with **one domain only**.

## Recommended domain

Use only one public domain on Coolify:

```text
https://wifi.yourhotel.com
```

Only assign this domain to the **gateway** service.
Do **not** assign domains to backend, frontend, db, redis, or worker.

## URLs

- Portal: `https://wifi.yourhotel.com/portal?hotel=demo-hotel`
- Admin: `https://wifi.yourhotel.com/admin`
- API: `https://wifi.yourhotel.com/api`
- Health: `https://wifi.yourhotel.com/health`

## Files included

- `compose.yaml` -> main Coolify file
- `docker-compose.yml` -> same file for compatibility
- `deploy/nginx.conf` -> single-domain reverse proxy
- `.env.coolify.example` -> required environment variables
- `backend/Dockerfile`
- `frontend/Dockerfile`

## Coolify deploy steps

### 1. Create resource
- Coolify -> **New Resource**
- Choose **Docker Compose Empty**
- Paste the content of `compose.yaml`

### 2. Add environment variables
Add these in Coolify:

```text
POSTGRES_PASSWORD=change-me-now
SECRET_KEY=replace-with-a-long-random-secret
ENCRYPTION_KEY=01234567890123456789012345678901
```

### 3. Set domain
Assign domain only to:
- `gateway` -> `https://wifi.yourhotel.com`

### 4. Deploy
Deploy the stack.

### 5. Seed demo data
Run the `seed` service once.

## Demo credentials

- Admin: `admin@demo.local` / `admin123`
- Guest room login: `101` + `Park`
- Guest voucher login: `DEMO101`

## Notes

- `gateway` handles `/`, `/portal`, `/admin`, `/api`
- `frontend` stays internal only
- `backend` stays internal only
- `db` and `redis` stay internal only
- MikroTik captive portal redirect should point to:

```text
https://wifi.yourhotel.com/portal
```
