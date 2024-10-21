FROM python:3.11-slim

ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ENV GITHUB_REPOSITORY=${GITHUB_REPOSITORY}
ENV GITHUB_SHA=${GITHUB_SHA}

WORKDIR /app

RUN apt-get update \
    && pip install poetry==1.8.4 \
    && apt-get install -y --no-install-recommends git ssh-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN poetry config virtualenvs.create false

COPY . /app/

RUN chmod +x /app/entrypoint.sh

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry install --no-root

ENTRYPOINT ["/app/entrypoint.sh"]
