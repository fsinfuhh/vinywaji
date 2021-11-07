FROM docker.io/tiangolo/uvicorn-gunicorn:python3.8-slim

# add system dependencies
RUN pip3 install pipenv
WORKDIR /app

# install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system --ignore-pipfile

# add remaining sources
COPY src /app/
COPY docker/prestart.sh /app/
RUN ln -sf /app/bitbots_drinks/asgi.py /app/main.py

# setup recommended container config
RUN mkdir /app/data
ENV DJANGO_CONFIGURATION=Prod
ENV BBD_DB_PATH=/app/data/db.sqlite

# add additional metadata
VOLUME /app/data
EXPOSE 80/tcp
