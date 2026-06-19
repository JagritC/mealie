# Runtime Baseline

- Entry: `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml -f docker/docker-compose.arcanist.yml up --build -d`
- Primary URL: `http://localhost:9091/`
- Ready route: `GET /api/app/about/startup-info`
- Seeded admin: `changeme@example.com` / `MyPassword`
- First authenticated route on a fresh volume: `/admin/setup`
- Smoke proof for DB-backed startup: `GET /api/app/about/startup-info`
- Smoke proof for authenticated app state: `POST /api/auth/token` then `GET /api/users/self`

# Notes

- The Arcanist override switches the app to PostgreSQL and waits on `pg_isready` before starting the web container.
- A fresh volume triggers Alembic migrations and default user/group/household creation during app startup.
- SMTP, LDAP, OIDC, and OpenAI stay disabled in this baseline because no corresponding env values are required to boot the core product flow.
