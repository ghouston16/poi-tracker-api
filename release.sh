#!/bin/sh
alembic upgrade head
gunicorn --bind 0.0.0.0:$PORT app.main:app -w 4 -k uvicorn.workers.UvicornWorker