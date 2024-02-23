FROM python:3.11.4-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app
