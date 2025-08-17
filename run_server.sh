#!/bin/bash

# Run the application
echo "Starting FastAPI application..."
echo "Access the API at http://localhost:8000"
uv venv .venv
source .venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > uvicorn.log 2>&1 &
