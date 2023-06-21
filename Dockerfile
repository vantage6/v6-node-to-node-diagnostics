# basic python3 image as base
FROM continuumio/miniconda3

# This is a placeholder that should be overloaded by invoking
# docker build with '--build-arg PKG_NAME=...'
ARG PKG_NAME="n2n_diagnostics"
ENV PYTHON_PATH="/opt/conda/envs/py310/bin/python"
RUN echo $PYTHON_PATH

RUN conda create -y -n py310 python=3.10

RUN apt update &&  apt install -y iproute2 traceroute iputils-ping curl

# install federated algorithm
COPY . /app
RUN $PYTHON_PATH -m pip install /app

ENV PKG_NAME=[${PKG_NAME}]

# Tell docker to execute `docker_wrapper()` when the image is run.
CMD $PYTHON_PATH -c "from vantage6.tools.docker_wrapper import docker_wrapper; docker_wrapper('${PKG_NAME}')"