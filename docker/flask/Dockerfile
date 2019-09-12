FROM python:3.7.0-slim

LABEL maintainer "Alexandre Pape <alexandre.pape@epitech.eu>"

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    && apt-get -y install apt-utils gunicorn libpq-dev python3-dev \
    && apt-get autoremove -y \
    && apt-get clean all

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip -r requirements.txt

COPY . .

CMD gunicorn app:app --bind 0.0.0.0:8000