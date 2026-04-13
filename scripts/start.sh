#!/bin/bash

logs=logs/pv_simulation.log

# Create the logs directory if it doesn't exist
mkdir -p logs

# Number of Gunicorn workers: each handles one simulation at a time.
# Default 4 workers = 4 concurrent PV simulations.
# Tune based on available RAM (~2-4 GB per worker).
WORKERS=${GUNICORN_WORKERS:-10}
TIMEOUT=${GUNICORN_TIMEOUT:-600}

cd /pv_simulation/scripts

exec gunicorn \
    --bind 0.0.0.0:8082 \
    --workers "$WORKERS" \
    --timeout "$TIMEOUT" \
    --worker-class sync \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    start:app 2>&1 | tee -a "/pv_simulation/${logs}"
