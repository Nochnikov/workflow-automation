#!/bin/sh

set -e

HOST=${APP_HOST:-0.0.0.0}
PORT=${APP_PORT:-8001}
PROJECT_PATH=${PROJECT_PATH:-app}

echo "Starting the development server"
exec uvicorn \
        --reload \
        --host ${HOST} \
        --port ${PORT} \
        --log-level debug \
        --no-access-log \
        ${PROJECT_PATH}.main:app

