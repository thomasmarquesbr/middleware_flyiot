FROM ubuntu:latest
LABEL maintainer="Thomás Marques"
RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip \
    && mkdir /opt/discovery \
    && pip install zeroconf
COPY . /opt/discovery
WORKDIR /opt/discovery
ENTRYPOINT ["python3", "start.py"]