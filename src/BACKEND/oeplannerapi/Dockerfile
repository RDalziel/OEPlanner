# Use Python 3.10 slim image
FROM python:3.10-slim

# Create and change to the app directory
WORKDIR /app

COPY oeplannertasks oeplannertasks

WORKDIR /app/oeplannerapi

# Copy pyproject.toml and poetry.lock
COPY oeplannerapi/pyproject.toml oeplannerapi/poetry.lock ./

# Install poetry
RUN pip install poetry

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy source code
COPY oeplannerapi .

# Expose port 80
EXPOSE 80

# Start uvicorn with poetry
CMD ["poetry", "run", "uvicorn", "oeplannerapi.main:app", "--host", "0.0.0.0", "--port", "80"]