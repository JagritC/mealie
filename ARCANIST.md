# Arcanist Guide

Mealie is a FastAPI backend plus a Nuxt frontend. The production Docker path serves the generated SPA from the backend container on port `9000`; the Arcanist runtime publishes it on `http://localhost:9091` with PostgreSQL enabled through `docker/docker-compose.arcanist.yml`.

## Build, Test, Lint

- Install repo deps: `bash .arcanist/setup.sh`
- Start local support services: `docker compose -f docker/docker-compose.dev.yml up`
- Run the backend locally: `uv run python mealie/app.py`
- Run backend checks: `uv run ruff format . --check && uv run ruff check mealie && uv run mypy mealie`
- Run focused backend tests: `DB_ENGINE=sqlite uv run pytest tests/unit_tests tests/integration_tests/admin_tests/test_admin_about.py tests/integration_tests/user_tests/test_user_login.py`
- Run the frontend checks: `cd frontend && yarn nuxt prepare && yarn lint --max-warnings=0 && yarn test:ci`
- Validate the container stack config: `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml -f docker/docker-compose.arcanist.yml config >/dev/null`
- Runtime smoke with the seeded admin: `bash .arcanist/verify/runtime-login.sh`

## Repo Gotchas

- The first boot migrates the database and seeds the default admin `changeme@example.com` / `MyPassword`; a fresh login lands on `/admin/setup`.
- The production image is the authoritative sandbox runtime here. It builds the frontend into the Python package and serves a single web app on container port `9000`.
- `docker/docker-compose.arcanist.yml` is the runtime override that flips the app from SQLite to PostgreSQL and waits for the DB healthcheck.
- Future schema changes still need the repo’s code generation flow; use `task dev:generate` in environments where `task` is installed.
- Locale changes should stay limited to `frontend/app/lang/messages/en-US.json`; the other locales are Crowdin-managed.

## Instruction Index

- `.github/copilot-instructions.md` — “Mealie Development Guide for AI Agents”; repo-wide architecture, naming, testing, and review guidance.
- `.github/pull_request_template.md` — repo PR body structure and required sections, including testing and AI/LLM disclosure.
