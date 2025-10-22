#!/bin/bash

echo "========================================"
echo "  Agent Market - Starting Application"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import streamlit" &> /dev/null
then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo ""
echo "Starting Agent Market..."
echo "The app will open in your browser automatically."
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

streamlit run app.py

