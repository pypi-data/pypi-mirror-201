FROM python:3.11-alpine3.17

RUN apk update && apk add --update postgresql-dev gcc python3-dev musl-dev libffi-dev

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app /
