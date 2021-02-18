# Setup
In order to test out a production-style stack for dev purposes, run the following: 
1. Populate the `.env` file based on `.env.example`
2. Start up the stack: `docker-compose up -d`
3. `docker-compose exec birdspotter python manage.py migrate`