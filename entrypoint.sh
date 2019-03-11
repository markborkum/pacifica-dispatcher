#!/bin/bash
if [[ -z $PEEWEE_DATABASE_URL ]] ; then
  if [[ $PEEWEE_USER && $PEEWEE_PASS ]]; then
    PEEWEE_USER_PART="${PEEWEE_USER}:${PEEWEE_PASS}@"
  fi
  if [[ $PEEWEE_PORT ]] ; then
    PEEWEE_ADDR_PART="${PEEWEE_ADDR}:${PEEWEE_PORT}"
  else
    PEEWEE_ADDR_PART=$PEEWEE_ADDR
  fi
  PEEWEE_DATABASE_URL="${PEEWEE_PROTO}://${PEEWEE_USER_PART}${PEEWEE_ADDR_PART}/${PEEWEE_DATABASE}"
fi
mkdir ~/.pacifica-dispatcher/
printf '[database]\npeewee_url = '${PEEWEE_DATABASE_URL}'\n' > ~/.pacifica-dispatcher/config.ini
pacifica-dispatcher-cmd dbsync
uwsgi \
  --http-socket 0.0.0.0:8050 \
  --master \
  --die-on-term \
  --wsgi-file /usr/src/app/pacifica/dispatcher/wsgi.py "$@"
