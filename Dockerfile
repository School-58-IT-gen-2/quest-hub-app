FROM thehale/python-poetry as poetry-base
WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true \
	&& poetry install --only main


FROM python:3.12-slim
WORKDIR /app
COPY --from=poetry-base /app /app
ENV PATH="/app/.venv/bin:$PATH"


COPY main.py main.py
COPY fastapi_example/ fastapi_example/