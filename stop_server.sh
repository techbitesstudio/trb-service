#!/bin/bash

# Find and kill the uvicorn process
PID=$(pgrep -f "uvicorn main:app")

if [ -z "$PID" ]; then
  echo "No running uvicorn server found."
else
  echo "Stopping uvicorn server (PID: $PID)..."
  kill -9 $PID
  echo "Server stopped successfully."
fi
