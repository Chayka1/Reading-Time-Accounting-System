# The Reading Time Metering System project

## In this repository, you'll find a system for tracking reading time and managing reading sessions. The system includes a Django Rest Framework (DRF) API to manage books, reading sessions, and provides statistics on reading time. Additionally, it utilizes Celery for asynchronous tasks to collect and update user reading statistics. The repository also includes comprehensive tests using Pytest to ensure the functionality of the API and asynchronous tasks.

## Application setup

```bash
pip install pipenv

pipenv shell
pipenv sync --dev

python src/manage.py runserver
```

## Celery workers start

```bash
pipenv shell
celery -A config worker --loglevel=info
```
