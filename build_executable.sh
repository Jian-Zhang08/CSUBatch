#!/bin/bash

# Install PyInstaller if not already installed
echo "Installing PyInstaller..."
pip install pyinstaller

# Build the executable
echo "Building CSUbatch executable for Linux..."
pyinstaller --name=CSUbatch --onefile --add-data="benchmark:benchmark" --add-data="performance:performance" src/main.py

# Create required directories
echo "Creating required directories..."
mkdir -p dist/benchmark
mkdir -p dist/performance
mkdir -p dist/results

# Copy required files
echo "Copying required files..."
cp benchmark/batch_job.py dist/benchmark/
cp performance/*.py dist/performance/

# Create an empty __init__.py if it doesn't exist
touch dist/performance/__init__.py

# Make scripts executable
echo "Setting executable permissions..."
chmod +x dist/CSUbatch
chmod +x dist/benchmark/batch_job.py

echo "Build complete!"
echo "You can find the executable at dist/CSUbatch"
echo "To run CSUbatch, execute: ./dist/CSUbatch" 