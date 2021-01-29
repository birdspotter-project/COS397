FROM devinchristianson/birdspotter:base-deps
WORKDIR /usr/src/app
COPY ./birdspotter ./birdspotter
COPY ./manage.py .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]