FROM osgeo/gdal:ubuntu-small-3.2.1 AS base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y python3 python3-pip \
    && pip3 install --upgrade pip
ONBUILD ADD ./requirements.txt .
ONBUILD RUN pip3 install -r requirements.txt && rm requirements.txt

FROM base as dev 
# NOTE needs to be build with context in root of app directory due to onbuild add & install of requirements.txt
RUN pip --disable-pip-version-check install 'prospector==1.3.1' 'bandit==1.7.0' 'coverage==5.4'
RUN apt remove python

FROM base AS prod-deps
HEALTHCHECK CMD curl --no-keepalive -s -f -I localhost:8000/health/
RUN apt update --fix-missing && apt install -y libpq-dev python-dev \
    && pip3 --disable-pip-version-check --no-cache-dir install 'psycopg2==2.8.6'

FROM ubuntu:20.04 AS prod
COPY --from=prod-deps /usr/local/lib/python3.8/dist-packages/ /usr/local/lib/python3.8/dist-packages/
COPY --from=prod-deps /usr/lib/python3.8/ /usr/lib/python3.8/
COPY --from=prod-deps /usr/lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/
COPY --from=prod-deps /usr/bin/python3 /usr/bin/python3
WORKDIR /app
RUN mkdir /static
COPY ./birdspotter ./birdspotter
COPY ./manage.py .
ENV PROD_DB=true
ENV PROD_EMAIL=true
EXPOSE 8000
RUN python3 manage.py collectstatic
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]