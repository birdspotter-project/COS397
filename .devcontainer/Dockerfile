FROM osgeo/gdal:ubuntu-small-3.2.1 AS base
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update -y && apt install -y python3 python3-pip \
    && pip3 install --upgrade pip
ONBUILD ADD ./requirements.txt .
ONBUILD RUN pip3 install -r requirements.txt && rm requirements.txt

FROM base as dev 
# NOTE needs to be build with context in root of app directory due to onbuild add & install of requirements.txt
RUN pip --disable-pip-version-check install 'prospector==1.3.1' 'bandit==1.7.0' 'coverage==5.4'

FROM dev as devcontainer
RUN apt update -y && apt install -y git locales sudo fish && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
RUN adduser --disabled-password --gecos "" vscode && usermod -aG sudo vscode \
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode

RUN apt install -y libpq-dev python-dev \
    && pip3 --disable-pip-version-check --no-cache-dir install 'psycopg2==2.8.6'
