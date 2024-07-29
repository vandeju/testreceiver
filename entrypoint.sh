#!/bin/bash

# Script that is called when the container is started

echo "Starting app"
# uvicorn app:app --host 0.0.0.0 --port 8080
# sleep infinity
python sender.py 