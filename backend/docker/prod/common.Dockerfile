FROM python:3.11-slim
WORKDIR /app

RUN apt update && apt install gcc python3-dev libmagic1 -y
RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY . .
