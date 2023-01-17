FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/
COPY main.py /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN rm -Rf /root/.cache/pip

RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
