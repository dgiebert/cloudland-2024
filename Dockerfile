FROM registry.suse.com/bci/python:3.12

COPY . /opt
WORKDIR /opt

RUN zypper in -y python3-gpiod \
    && zypper clean --all \
    && pip install -r requirements.txt
