FROM python:3.13-slim

# Install uv (pinned for reproducible builds).
COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/web-backend \
    UV_PROJECT_ENVIRONMENT=/web-backend/.venv

WORKDIR /web-backend

# Copy dependency manifests first to leverage Docker layer caching.
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache --no-dev

COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini ./

# Run as a non-root user.
RUN useradd --create-home appuser && chown -R appuser:appuser /web-backend
USER appuser

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]