FROM python:3.10-slim

WORKDIR /inquest-api

COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0", "--port=80", "--no-reload"]
