# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code

ADD . /code/
RUN pip install --upgrade pip && \
    pip install pip-tools && \
    ls -R && \
    pip-compile -q ./requirements/requirements.in --output-file ./requirements.txt && \
    pip install --no-cache-dir -r ./requirements.txt
COPY . /code/