#!/usr/bin/env bash

echo "Starting Company Brain..."

uvicorn backend.main:app --host 0.0.0.0 --port $PORT
