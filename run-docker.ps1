# Check if Docker is installed
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Error "Error: Docker is not installed or not in the PATH"
    Write-Host "Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
}

# Check if docker-compose is installed
if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Error "Error: docker-compose is not installed or not in the PATH"
    Write-Host "Please install docker-compose: https://docs.docker.com/compose/install/"
    exit 1
}

# Create results directory if it doesn't exist
if (-not (Test-Path -Path "results")) {
    New-Item -Path "results" -ItemType Directory
}

# Build and run the container
Write-Host "Building and starting CSUbatch container..."
docker-compose up --build -d

# Attach to the container
Write-Host "Attaching to CSUbatch. Use Ctrl+C to exit."
docker attach csubatch

# Clean up when done
Write-Host "Stopping CSUbatch container..."
docker-compose down 