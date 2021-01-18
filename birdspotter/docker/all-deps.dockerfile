FROM devinchristianson/birdspotter:base-deps
ADD ./requirements.txt .
RUN pip3 install -r requirements.txt && rm requirements.txt