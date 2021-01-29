FROM devinchristianson/birdspotter:all-deps
RUN apt update -y && apt install -y git locales sudo fish && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && locale-gen
RUN adduser --disabled-password --gecos "" vscode && usermod -aG sudo vscode \
    && echo vscode ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/vscode \
    && chmod 0440 /etc/sudoers.d/vscode
COPY birdspotter/requirements.txt /tmp/requirements.txt
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt 

