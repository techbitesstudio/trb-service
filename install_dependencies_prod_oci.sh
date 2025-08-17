#!/bin/bash

# This script sets up a virtual environment, installs dependencies,
# and runs the FastAPI application locally.

# The first time you run this, pyppeteer will download a compatible
# version of Chromium. This may take a few minutes.

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv .venv
fi

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install fastapi uvicorn[standard] pyppeteer transformers

uv pip install torch --index-url https://download.pytorch.org/whl/cpu

uv pip freeze > requirements.txt