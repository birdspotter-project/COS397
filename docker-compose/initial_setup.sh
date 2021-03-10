#!/bin/bash
set -e

docker-compose exec -d birdspotter python3 manage.py makemigrations
docker-compose exec -d birdspotter python3 manage.py migrate
docker-compose exec -d birdspotter python3 manage.py create_groups
docker-compose exec -d birdspotter python3 manage.py create_inbox
docker-compose exec -d birdspotter python3 manage.py createsuperuser --noinput
