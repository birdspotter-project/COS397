# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.154.2/containers/python-3-miniconda/.devcontainer/base.Dockerfile

FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3
# Fix conda install
RUN sudo chown -R vscode:vscode /opt/conda
# Install GDAL
RUN conda install -y gdal
# Update Numpy to correct downgrade due to GDAL
RUN conda update -y numpy
COPY birdspotter/requirements.txt /tmp/requirements.txt~
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/requirements.txt 

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>
