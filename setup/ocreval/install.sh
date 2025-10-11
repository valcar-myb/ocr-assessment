#!/bin/bash
# Installation script for ocreval on Linux/macOS

set -e

echo "======================================"
echo "ocreval Installation Script"
echo "======================================"
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Detected macOS"
    echo ""
    
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "Installing ocreval via Homebrew..."
        brew install eddieantonio/eddieantonio/ocreval
        echo "✓ Installation complete!"
    else
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Detected Linux"
    echo ""
    
    # Install build dependencies
    echo "Step 1: Installing build dependencies..."
    sudo apt update
    sudo apt install -y build-essential
    
    # Try to install libutf8proc-dev
    echo "Step 2: Installing libutf8proc-dev..."
    if sudo apt install -y libutf8proc-dev; then
        echo "✓ libutf8proc-dev installed via apt"
    else
        echo "Installing libutf8proc from source..."
        TEMP_DIR=$(mktemp -d)
        cd "$TEMP_DIR"
        curl -OL https://github.com/JuliaStrings/utf8proc/archive/v1.3.1.tar.gz
        tar xzf v1.3.1.tar.gz
        cd utf8proc-1.3.1/
        make
        sudo make install
        sudo ldconfig
        cd -
        rm -rf "$TEMP_DIR"
        echo "✓ libutf8proc installed from source"
    fi
    
    # Clone and build ocreval
    echo "Step 3: Building ocreval..."
    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"
    git clone https://github.com/eddieantonio/ocreval.git
    cd ocreval
    make
    
    echo "Step 4: Installing ocreval..."
    sudo make install
    
    cd -
    rm -rf "$TEMP_DIR"
    
    echo "✓ Installation complete!"
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo ""
echo "======================================"
echo "Verifying installation..."
echo "======================================"

if command -v accuracy &> /dev/null; then
    echo "✓ ocreval installed successfully!"
    echo ""
    echo "Available tools:"
    which accuracy
else
    echo "❌ Installation failed. 'accuracy' command not found."
    exit 1
fi

echo ""
echo "======================================"
echo "Installation complete!"
echo "======================================"

