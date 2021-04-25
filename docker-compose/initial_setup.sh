#!/bin/bash
set -e

docker-compose exec birdspotter python3 manage.py migrate
docker-compose exec birdspotter python3 manage.py create_groups
docker-compose exec birdspotter python3 manage.py create_inbox
docker-compose exec birdspotter python3 manage.py createsuperuser --noinput
