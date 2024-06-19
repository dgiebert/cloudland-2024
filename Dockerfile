ARG PYTHON_VERSION=3.12
FROM registry.suse.com/bci/python:${PYTHON_VERSION} as builder

RUN zypper in -y gcc && python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . /opt
WORKDIR /opt
RUN pip install -r requirements.txt


FROM registry.suse.com/bci/python:${PYTHON_VERSION}
COPY --from=builder /opt /opt
ENV PATH="/opt/venv/bin:$PATH"
ENTRYPOINT ["python3", "opt/src/main.py"]
