#!/bin/bash

echo "========================================"
echo "  Web3 MarketMind 4.0 - Quick Start"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo ""

# Create necessary directories
mkdir -p models
mkdir -p data
echo ""

# Run the application
echo "========================================"
echo "  Starting Web3 MarketMind 4.0..."
echo "========================================"
echo ""
echo "  Access the app at: http://localhost:8501"
echo "  Demo credentials: demo / demo123"
echo ""
echo "  Press Ctrl+C to stop the server"
echo "========================================"
echo ""

streamlit run app_v4.py
