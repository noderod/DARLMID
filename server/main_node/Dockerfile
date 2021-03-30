FROM python:3.9-alpine


COPY helper.py             /expert_seas/helper.py
COPY helper_postgres.py    /expert_seas/helper_postgres.py
COPY traffic.py            /expert_seas/traffic.py
COPY create_tables.py      /expert_seas/create_tables.py
COPY html                  /expert_seas/html


RUN apk update &&\
    apk add bash curl gcc musl-dev postgresql-dev python3-dev &&\
    pip3 install --upgrade pip && pip3 install aiohttp aioredis bleach gunicorn psycopg2 &&\
    mkdir /expert_seas/images


WORKDIR /expert_seas
