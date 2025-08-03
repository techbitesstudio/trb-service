#!/bin/bash

# This script sets up a virtual environment, installs dependencies,
# and runs the FastAPI application locally.

# The first time you run this, pyppeteer will download a compatible
# version of Chromium. This may take a few minutes.

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
_pip_out=$(pip install -r requirements.txt)

# Run the application
echo "Starting FastAPI application..."
echo "Access the API at http://localhost:8000"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
