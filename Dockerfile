FROM registry.suse.com/bci/python:3.12

RUN zypper in -y libgpiod

COPY . /opt

WORKDIR /opt
RUN pip install -r requirements.txt
