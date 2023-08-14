FROM python:3.10-slim
# Create and change to the app directory
WORKDIR /app

COPY oeplannertasks oeplannertasks

WORKDIR /app/oeplannerworker

# Copy pyproject.toml and poetry.lock
COPY oeplannerworker/pyproject.toml oeplannerworker/poetry.lock ./

# Install poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy source code
COPY OEPlannerWorker .

CMD ["poetry", "run", "celery", "-A", "oeplannerworker.main", "worker", "--loglevel=info"]