FROM registry.suse.com/bci/python:3.12

COPY . /opt
WORKDIR /opt

RUN zypper in -y libgpiod \
    && pip install -r requirements.txt
