#!/bin/sh
set -e
alembic upgrade head
python app.py