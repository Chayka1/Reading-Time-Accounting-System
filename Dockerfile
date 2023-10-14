FROM python:latest

WORKDIR /app/

COPY . .

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools \
    && pip install pipenv \
    && pip install watchdog


RUN pipenv sync --dev --system

CMD python src/manage.py migrate && python src/manage.py runserver 0.0.0.0:8000