FROM python:3.11-slim

ENV PYTHONPATH="/app/src/:${PYTHONPATH}" \
    POETRY_VERSION=1.8.4 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /app

RUN apt-get update \
    && pip install poetry==${POETRY_VERSION} \
    && apt-get install -y --no-install-recommends git ssh-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml /app/

COPY . /app/

RUN chmod +x /app/entrypoint.sh

RUN poetry install --only main

ENTRYPOINT ["/app/entrypoint.sh"]
