#!/bin/bash

# This script sets up a virtual environment, installs dependencies,
# and runs the FastAPI application locally.

# The first time you run this, pyppeteer will download a compatible
# version of Chromium. This may take a few minutes.

sudo apt update
sudo apt install python3-pip

sudo apt install python3.11-venv

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip3 install uv

uv pip install fastapi uvicorn[standard] pyppeteer transformers

uv pip install torch --index-url https://download.pytorch.org/whl/cpu

uv pip freeze > requirements.txt