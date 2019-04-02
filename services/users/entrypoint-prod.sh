#!/bin/sh

echo "waiting for postgres user server"

while ! nc -z users-db 5432; do
  sleep 0.1
done

echo "Postgres user server started"

gunicorn -b 0.0.0.0:5002 manage:app
