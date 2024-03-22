FROM python:3

WORKDIR /usr/src/app

ENV DB_HOST="10.0.2.15"\
 DB_PORT="5432"\
 DB_USER="user"\
 DB_PASS="user"\
 DB_NAME="user"

RUN pip install psycopg2
RUN useradd newuser
USER newuser

COPY . /PG

CMD [ "python", "/PG/scrypt.py" ]
