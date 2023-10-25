FROM python:3.11-slim

WORKDIR /app
RUN apt update && apt install gcc python3-dev -y

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
