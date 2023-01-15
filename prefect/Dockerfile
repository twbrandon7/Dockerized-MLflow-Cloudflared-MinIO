FROM python:3.8-slim

WORKDIR /root
ENV DEBIAN_FRONTEND=noninteractive

RUN python -m pip install pip --upgrade

RUN pip install --no-cache-dir "prefect==2.7.8"

RUN rm -Rf /root/.cache/pip

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY ./setup.py /root

CMD ["bash"]
