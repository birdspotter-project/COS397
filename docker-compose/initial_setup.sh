#!/bin/bash
set -e

docker-compose exec -d slurmctld /usr/bin/sacctmgr --immediate add cluster name=linux
docker-compose restart slurmdbd slurmctld

docker-compose exec -d birdspotter python3 manage.py makemigrations
docker-compose exec -d birdspotter python3 manage.py migrate
docker-compose exec -d birdspotter python3 manage.py createsuperuser --noinput