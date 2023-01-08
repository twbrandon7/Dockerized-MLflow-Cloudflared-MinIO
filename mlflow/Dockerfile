FROM python:3.8-slim

WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive

RUN python -m pip install pip --upgrade

RUN pip install --no-cache-dir mlflow[extras]

RUN rm -Rf /root/.cache/pip

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["bash"]
