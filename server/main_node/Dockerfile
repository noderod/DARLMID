FROM python:3.9-alpine


COPY helper.py             /DARLMID/helper.py
COPY helper_postgres.py    /DARLMID/helper_postgres.py
COPY traffic.py            /DARLMID/traffic.py
COPY data_combiner.py      /DARLMID/data_combiner.py
COPY startup.sh            /DARLMID/startup.sh
COPY create_tables.py      /DARLMID/create_tables.py
COPY html                  /DARLMID/html
COPY circuits              /DARLMID/circuits

RUN apk update &&\
    apk add bash curl gcc musl-dev postgresql-dev python3-dev &&\
    pip3 install --upgrade pip && pip3 install aiohttp aioredis bleach gunicorn psycopg2 &&\
    mkdir /DARLMID/data && mkdir /DARLMID/data/positive /DARLMID/data/negative &&\
    chmod +x /DARLMID/startup.sh


WORKDIR /DARLMID
