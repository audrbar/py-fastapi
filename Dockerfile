# ------- Stage 1: Base Setup (Alpine) -----
FROM python:3.12-alpine AS python_base

# Python optimizations
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

# Install PostgreSQL client libraries (required for psycopg2)
RUN apk add --no-cache postgresql-libs

WORKDIR /app

# ------ Stage 2: Builder ------
FROM python_base AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Install build dependencies for PostgreSQL driver
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    postgresql-dev

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Remove build dependencies to keep image small
RUN apk del .build-deps

# ------ Stage 3: Dev Environment ------
FROM python_base AS dev
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Add common debug tools for local troubleshooting
RUN apk add --no-cache \
    curl \
    git \
    vim \
    wget \
    bind-tools \
    netcat-openbsd \
    procps

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

COPY pyproject.toml uv.lock ./
COPY app ./app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# -------- Stage 4: Production (The Tiny Image) ------
FROM python_base AS prod

RUN addgroup -S appuser && adduser -S appuser -G appuser -h /app
USER appuser

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY app ./app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
