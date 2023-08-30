FROM python:3.10-slim

WORKDIR /turbine-api

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

CMD sleep 10 && python3 daemon.py
