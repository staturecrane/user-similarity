FROM python:3.6.1-slim

RUN apt-get update && apt-get install -y \
    bzip2 \
    curl \
    ca-certificates \
    git \
    libx11-6 \
    sudo \
    unzip

WORKDIR /app
ENV PYTHONPATH /app 

COPY requirements.txt /app
RUN pip3 install -q -r requirements.txt

COPY similarity_api/ /app/similarity_api/

EXPOSE 5000

CMD gunicorn similarity_api.main:APP -b 0.0.0.0:5000 --log-level DEBUG
