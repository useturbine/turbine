FROM python:3.11-slim
RUN apt update && apt install gcc python3-dev -y

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
