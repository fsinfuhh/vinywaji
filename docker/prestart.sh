#!/usr/bin/sh
set -e

./src/manage.py tailwind install
./manage.py check --deploy
./manage.py tailwind build
./manage.py collectstatic --no-input
./manage.py migrate
