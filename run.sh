#!/bin/bash
echo "Starting Windows Pets..."

# Install dependency
python3 -m pip install PyQt6 --quiet 2>/dev/null || pip3 install PyQt6 --quiet

# Run the app
python3 "$(dirname "$0")/main.py"
