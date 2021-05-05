# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /courses-app
COPY requirements.txt /courses-app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /courses-app/