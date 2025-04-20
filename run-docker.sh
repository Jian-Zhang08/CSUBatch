#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in the PATH"
    echo "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed or not in the PATH"
    echo "Please install docker-compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create results directory if it doesn't exist
mkdir -p results

# Build and run the container
echo "Building and starting CSUbatch container..."
docker-compose up --build -d

# Attach to the container
echo "Attaching to CSUbatch. Use Ctrl+C to exit."
docker attach csubatch

# Clean up when done
echo "Stopping CSUbatch container..."
docker-compose down 