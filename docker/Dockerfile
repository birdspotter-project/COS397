FROM osgeo/gdal:ubuntu-small-3.2.1 AS base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y python3 python3-pip \
    && pip3 install --upgrade pip
ONBUILD ADD ./requirements.txt .
ONBUILD RUN pip3 install -r requirements.txt && rm requirements.txt

FROM base as dev 
# NOTE needs to be build with context in root of app directory due to onbuild add & install of requirements.txt
RUN pip --disable-pip-version-check install 'prospector==1.3.1' 'bandit==1.7.0' 'coverage==5.4'

FROM base AS prod
RUN apt install -y libpq-dev \
    && pip3 --disable-pip-version-check --no-cache-dir install python-dev 'psycopg2==2.8.6'
WORKDIR /usr/src/app
COPY ./birdspotter ./birdspotter
COPY ./manage.py .
ENV PROD_DB=true
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]