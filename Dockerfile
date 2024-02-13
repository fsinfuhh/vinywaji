FROM docker.io/tiangolo/uvicorn-gunicorn:python3.10-slim

# add system dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update &&\
    apt-get install -y --no-install-recommends git &&\
    apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache pipenv psycopg2-binary
WORKDIR /app

# install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --ignore-pipfile

# add remaining sources
COPY src /app/
COPY docker/prestart.sh /app/
RUN ln -sf /app/vinywaji/asgi.py /app/main.py

# setup recommended container config
RUN mkdir /app/data
ENV VW_DATABASE_URL=sqlite:///app/data/db.sqlite

# add additional metadata
VOLUME /app/data
EXPOSE 80/tcp
ENV APP_MODE=prod
