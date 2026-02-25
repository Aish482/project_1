#!/bin/bash

# Smart Logistics Platform - Unix Launch Script
# This script sets up the environment and runs the Streamlit app

echo ""
echo "================================================================================"
echo " Smart Logistics Management & Analytics Platform"
echo " Streamlit Dashboard Launch Script (Unix/Linux/Mac)"
echo "================================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "[✓] Python is installed: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
    echo "[✓] Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate
echo "[✓] Virtual environment activated"
echo ""

# Install/upgrade requirements
echo "[*] Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "[✓] Dependencies installed"
echo ""

# Run setup if needed
if [ "$1" == "--setup" ]; then
    echo "[*] Running setup wizard..."
    python setup.py --all
    echo ""
fi

# Run the Streamlit app
echo "[*] Starting Streamlit application..."
echo ""
echo "================================================================================"
echo " Dashboard will open in your default browser at: http://localhost:8501"
echo " Press CTRL+C to stop the server"
echo "================================================================================"
echo ""

streamlit run app.py
