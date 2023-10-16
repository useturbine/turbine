FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

CMD uvicorn turbine.api.app:app --host 0.0.0.0 --port 80
