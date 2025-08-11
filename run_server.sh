#!/bin/bash

# Run the application
echo "Starting FastAPI application..."
echo "Access the API at http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
