#!/bin/bash
# Quick Start Script for macOS/Linux

echo "=================================="
echo "Starting Face Recognition System"
echo "=================================="

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run the application
python3 run.py
