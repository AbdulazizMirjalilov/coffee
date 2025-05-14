# --------- Stage 1: Extract Dependencies ---------
FROM python:3.11-slim-bullseye

WORKDIR /app

ENV POETRY_VERSION=1.8

# install poetry and all dependices /////////
RUN pip install "poetry==$POETRY_VERSION" --no-cache-dir &&\
    poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-root --no-ansi

COPY . /app/

RUN chmod +x /app/scripts/*.sh
