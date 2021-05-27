# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && \
    pip install pip-tools && \
    pip-compile -q /code/spy/requirements/requirements.in --output-file /code/spy/requirements.txt && \
    pip install --no-cache-dir -r /code/spy/requirements.txt
COPY . /code/