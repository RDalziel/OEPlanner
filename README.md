# Over engineered Planner

# Getting Started

Follow these steps to setup the project locally:

### Install Dependencies

- Docker - Install Docker engine and docker-compose. See https://docs.docker.com/get-docker/
- Python - Install Python 3.10 or higher. 

### Install Poetry

```shell
pip install poetry
```


### Install Python packages 

In the repo root directory, install packages defined in pyproject.toml:

```shell
poetry install
```


# Docker Setup

This application utilizes Docker Compose to run the services in containers. The services include:

- **FastAPI** - The main FastAPI application that serves the API endpoints. 
- **Celery Worker** - The Celery worker that executes async tasks queued from FastAPI.
- **RabbitMQ** - The message broker used to send tasks between FastAPI and Celery.
- **Flower** - A web UI for monitoring and administrating Celery clusters and workers.

## Running the services

To start all the services, run:

```shell
docker-compose up
```

This will start the FastAPI service on port 8080, Celery worker, RabbitMQ on the default ports, and Flower on port 5555.

## Accessing the services

- FastAPI - http://localhost:8080/docs
- Worker - http://localhost:8081/health
- RabbitMQ - http://localhost:15672  (User: guest, Pass: guest)
- Flower - http://localhost:5555

RabbitMQ and Flower provide admin UI's to monitor queues, workers, tasks, etc.

The FastAPI service runs the main application and API endpoints.