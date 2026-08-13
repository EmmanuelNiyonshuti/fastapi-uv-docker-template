This is a simple starter template for a FastAPI application with PostgreSQL database.
Created as a demo project for this blog [docker containers: FastAPI + Postgresql](https://blog.niyonshutiemmanuel.com/blog/docker-containers-as-my-development-environment-fastapi-postgresql-1)

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)

### Run the app

1. Clone the repo and enter it.
2. Create your environment file:

   ```bash
   cp .env.template .env
   ```

3. Start the stack:

   ```bash
   docker compose up --build
   ```

4. Apply database migrations:

   ```bash
   docker compose exec web uv run alembic upgrade head
   ```

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

## Testing
Start the test database, then run the suite:

```bash
docker compose up -d db-test
uv sync --all-groups
uv run pytest
```

Override the connection defaults with environment variables (e.g.
`POSTGRES_SERVER`, `POSTGRES_PORT`, `POSTGRES_DB`).

Lint and format with ruff:

```bash
uv run ruff check .
uv run ruff format .
```

## Licence
MIT
