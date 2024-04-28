#!/bin/bash

# Set number of workers from environment variable or default to 4
WORKERS="${WORKERS:-2}"

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

# Set HOST and PORT from settings.toml or default values
SERVER="${SERVER:--0.0.0.0}"
PORT="${PORT:-8000}"

# Run gunicorn with the specified number of workers and bind address
gunicorn -w "$WORKERS" -b "$SERVER:$PORT" wsgi:app
