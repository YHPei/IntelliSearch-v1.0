#!/bin/bash
# ============================================================================
# Backend Quick Start Script (Linux/macOS)
# ============================================================================

echo "======================================"
echo "AI Search Engine - Backend Startup"
echo "======================================"
echo ""

# Check if in backend directory
if [ ! -f "main.py" ]; then
    echo "Error: Please run this script in the backend directory"
    exit 1
fi

# Check Python version
echo "Checking Python version..."
python3 --version

# Check virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Virtual environment not found, creating..."
    python3 -m venv venv
    echo "[OK] Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate
echo "[OK] Virtual environment activated"

# Install dependencies
echo ""
echo "Checking and installing dependencies..."
pip install -r requirements.txt
echo "[OK] Dependencies installed"

# Check .env file
echo ""
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found"
    echo "Please copy and configure API keys:"
    echo "  cp env.example .env"
    echo "  Then edit .env to add your API keys"
    exit 1
fi
echo "[OK] .env file configured"

# Start service
echo ""
echo "======================================"
echo "Starting backend service..."
echo "API URL: http://127.0.0.1:8000"
echo "API Docs: http://127.0.0.1:8000/docs"
echo "======================================"
echo ""

python main.py
