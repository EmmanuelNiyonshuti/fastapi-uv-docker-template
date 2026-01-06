# FastAPI + Postgres + uv (Docker Dev Setup)

This is a development environment for running FastAPI and PostgreSQL inside Docker containers using the [uv](https://docs.astral.sh/uv/) package manager. 

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/) installed on your machine.

1. **Clone the repo**
2. **Setup environment:** Create a `.env` file based on `.env.template`
3. **Run the app:**
   ```bash
   docker compose up
   ```

4. **Run migrations:**
```bash
docker compose exec web uv run alembic upgrade head
```
- API available at http://localhost:8000

- Swagger Docs at http://localhost:8000/docs

I documented it in detail here: [Docker Containers as My Development Environment](https://www.niyonshutiemmanuel.com/blog/docker-containers-as-my-development-environment-fastapi-postgresql-1)