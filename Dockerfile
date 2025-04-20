FROM python:3.9-slim

WORKDIR /app

# Copy the application files
COPY src/ /app/src/
COPY benchmark/ /app/benchmark/
COPY performance/ /app/performance/
COPY setup.py /app/
COPY README.md /app/

# Create results directory
RUN mkdir -p /app/results

# Install the application
RUN pip install -e .

# Make scripts executable
RUN chmod +x /app/src/main.py
RUN chmod +x /app/benchmark/batch_job.py

# Set the entrypoint
ENTRYPOINT ["python", "-m", "src.main"] 