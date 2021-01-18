FROM osgeo/gdal:ubuntu-small-3.2.1
RUN apt update -y && apt install -y python3 python3-pip \
    && pip3 install --upgrade pip