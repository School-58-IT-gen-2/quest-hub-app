FROM python:3.12-alpine AS builder

RUN pip install poetry==1.8.5

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.12-alpine AS runtime

WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apk add --no-cache curl

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY quest_hub_fastapi_server ./quest_hub_fastapi_server
COPY main.py ./main.py
RUN pip install python-logging-loki
COPY logs ./logs

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl -f https://questhub.pro/health || exit 1

ENTRYPOINT [ "python3", "main.py" ]