#!/usr/bin/env bash

PORT=${PORT:-10000}

echo "Starting server on port $PORT"

uvicorn backend.main:app --host 0.0.0.0 --port $PORT
