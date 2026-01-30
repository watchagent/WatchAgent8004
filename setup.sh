#!/bin/bash

# Watch8004 Setup Script
# This script sets up the development environment for Watch8004

set -e

echo "╔══════════════════════════════════════════════════════╗"
echo "║         Watch8004 ERC-8004 AI Agent Setup            ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "📋 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Check pip
echo ""
echo "📋 Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi
echo "✅ pip found: $(pip3 --version)"

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✅ Python dependencies installed"

# Check Node.js
echo ""
echo "📋 Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed. Installing Node.js is recommended for Foundry."
    echo "   You can continue, but some features may not work."
else
    echo "✅ Node.js found: $(node --version)"
fi

# Install Foundry
echo ""
echo "📦 Installing Foundry..."
if ! command -v forge &> /dev/null; then
    echo "   Downloading Foundry..."
    curl -L https://foundry.paradigm.xyz | bash
    
    # Source foundry env
    export PATH="$HOME/.foundry/bin:$PATH"
    
    echo "   Running foundryup..."
    foundryup
    
    echo "✅ Foundry installed"
else
    echo "✅ Foundry already installed: $(forge --version | head -n 1)"
fi

# Install OpenZeppelin contracts
echo ""
echo "📦 Installing OpenZeppelin contracts..."
cd contracts
if [ ! -d "lib/openzeppelin-contracts" ]; then
    forge install OpenZeppelin/openzeppelin-contracts --no-commit
    echo "✅ OpenZeppelin contracts installed"
else
    echo "✅ OpenZeppelin contracts already installed"
fi
cd ..

# Create .env file if it doesn't exist
echo ""
echo "⚙️  Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "   ⚠️  Please edit .env with your configuration"
else
    echo "✅ .env file already exists"
fi

# Create data directory
mkdir -p data
echo "✅ Created data directory"

# Summary
echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║                  Setup Complete! 🎉                   ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Start a local blockchain (in a separate terminal):"
echo "   anvil"
echo ""
echo "2. Run the Watch8004 demo:"
echo "   python3 main.py"
echo ""
echo "3. Open the web dashboard:"
echo "   open web/index.html"
echo ""
echo "For more information, see README.md"
echo ""
