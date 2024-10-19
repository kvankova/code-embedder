FROM python:3.11-slim

ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ENV GITHUB_REPOSITORY=${GITHUB_REPOSITORY}
ENV GITHUB_SHA=${GITHUB_SHA}

WORKDIR /app

RUN apt-get update \
    && pip install poetry==1.8.4

RUN poetry config virtualenvs.create false

COPY . /app/

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "/app/main.py"]