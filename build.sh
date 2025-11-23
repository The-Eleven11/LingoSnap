#!/bin/bash
# Build script for LingoSnap

set -e

echo "=== LingoSnap Build Script ==="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is required"
    exit 1
fi

# Check for required system packages
echo ""
echo "Checking for Tesseract OCR..."
if ! command -v tesseract &> /dev/null; then
    echo "Warning: Tesseract OCR not found. Install with:"
    echo "  sudo apt install tesseract-ocr"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install package in development mode
echo ""
echo "Installing LingoSnap in development mode..."
pip3 install -e .

echo ""
echo "=== Build Complete ==="
echo ""
echo "To run LingoSnap:"
echo "  lingosnap"
echo ""
echo "To run CLI tool:"
echo "  lingo -t 1"
echo ""
echo "For more information, see:"
echo "  - INSTALLATION.md for installation instructions"
echo "  - USAGE.md for usage guide"
echo "  - DEVELOPER.md for development guide"
