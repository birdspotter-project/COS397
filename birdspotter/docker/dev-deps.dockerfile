FROM devinchristianson/birdspotter:base-deps
# NOTE needs to be build with context in root of app directory due to onbuild add & install of requirements.txt
RUN pip --disable-pip-version-check install 'prospector==1.3.1' 'bandit==1.7.0' 'coverage==5.4'