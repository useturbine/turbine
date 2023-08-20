FROM python:3.10-slim

WORKDIR /inquest-api

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

CMD ["python3", "daemon.py"]
