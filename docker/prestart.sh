#!/usr/bin/sh
set -e

./manage.py check --deploy
./manage.py collectstatic --no-input
./manage.py migrate
