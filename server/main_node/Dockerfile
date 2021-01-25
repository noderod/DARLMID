FROM python:3.9-alpine


COPY traffic.py /expert_seas/traffic.py
COPY html       /expert_seas/html


RUN apk update &&\
    apk add bash curl gcc musl-dev postgresql-dev python3-dev &&\
    pip3 install --upgrade pip && pip3 install aiohttp gunicorn psycopg2 &&\
    mkdir /expert_seas/images


WORKDIR /expert_seas
