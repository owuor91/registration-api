#!/bin/sh
set -e
alembic upgrade head
gunicorn -c gunicorn.config.py wsgi:app