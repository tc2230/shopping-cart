FROM python:3.11-slim

RUN mkdir /deploy

COPY ./* /deploy/

RUN apt-get update && apt-get install nano

RUN pip install --no-cache-dir -r /deploy/requirements.txt

WORKDIR /deploy
