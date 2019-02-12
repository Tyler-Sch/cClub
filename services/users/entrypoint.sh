#!/bin/sh

echo "waiting for postgres user server"

while ! nc -z users-db 5432; do
  sleep 0.1
done

echo "Postgres user server started"

python manage.py run -h 0.0.0.0 -p 5002
