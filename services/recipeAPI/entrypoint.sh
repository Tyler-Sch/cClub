#!/bin/sh

echo "Waiting for postgres"

while ! nc -z recipes-db 5432; do
  sleep 0.1
done

echo "Postgres started"

python manage.py start
