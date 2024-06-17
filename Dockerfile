FROM python:3-alpine

WORKDIR /usr/src/app

ENV DB_HOST="db" \
    DB_PORT="5432" \
    DB_USER="user" \
    DB_PASS="user" \
    DB_NAME="user"

RUN pip install psycopg2-binary flask py-healthcheck
RUN adduser -D newuser
USER newuser 

COPY . /PG

CMD ["python", "/PG/scrypt.py"]
#
