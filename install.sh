#!/bin/bash

# CSUbatch installation script for Linux

echo "Installing CSUbatch..."

# Make sure Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check Python version
python3 --version

# Create and set up virtual environment (optional)
echo "Do you want to install CSUbatch in a virtual environment? (y/n)"
read use_venv

if [ "$use_venv" == "y" ] || [ "$use_venv" == "Y" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    if [ -f venv/bin/activate ]; then
        source venv/bin/activate
        echo "Virtual environment activated."
    else
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

# Install the package
echo "Installing CSUbatch package..."
pip install -e .

# Set executable permissions
chmod +x src/main.py
chmod +x benchmark/batch_job.py

echo ""
echo "CSUbatch has been installed successfully!"
echo ""

if [ "$use_venv" == "y" ] || [ "$use_venv" == "Y" ]; then
    echo "To use CSUbatch, activate the virtual environment with:"
    echo "  source venv/bin/activate"
    echo ""
    echo "You can then run CSUbatch with:"
    echo "  csubatch"
    echo "  or"
    echo "  python -m src.main"
else
    echo "You can now run CSUbatch with:"
    echo "  csubatch"
    echo "  or"
    echo "  python -m src.main"
fi

echo ""
echo "For more information, see the README.md file."
echo "" 