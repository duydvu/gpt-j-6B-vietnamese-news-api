#!/bin/sh

WORKER_TIMEOUT="${WORKER_TIMEOUT:-120}"

uvicorn \
      --workers 1 \
      --timeout-keep-alive "$WORKER_TIMEOUT" \
      --no-access-log \
      src.run_app:api_service --host 0.0.0.0 --port 5000
