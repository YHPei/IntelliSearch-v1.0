#!/bin/bash
# ============================================================================
# Frontend Quick Start Script (Linux/macOS)
# ============================================================================

echo "======================================"
echo "AI Search Engine - Frontend Startup"
echo "======================================"
echo ""

# Check if in frontend directory
if [ ! -f "package.json" ]; then
    echo "Error: Please run this script in the frontend directory"
    exit 1
fi

# Check Node.js version
echo "Checking Node.js version..."
node --version

# Check npm version
echo "Checking npm version..."
npm --version

# Check node_modules
if [ ! -d "node_modules" ]; then
    echo ""
    echo "node_modules not found, installing dependencies..."
    npm install
    echo "[OK] Dependencies installed"
else
    echo ""
    echo "[OK] Dependencies already installed"
fi

# Check .env file
echo ""
if [ ! -f ".env" ]; then
    echo "Note: .env file not found (optional)"
    echo "To customize API URL, copy from env.example:"
    echo "  cp env.example .env"
    echo ""
fi

# Start service
echo "======================================"
echo "Starting frontend development server..."
echo "URL: http://localhost:5173"
echo "======================================"
echo ""

npm run dev
