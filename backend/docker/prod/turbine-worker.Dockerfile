FROM python:3.10-slim

WORKDIR /turbine-worker

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

CMD celery --app turbine.worker.worker worker --loglevel=INFO
