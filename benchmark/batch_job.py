#!/usr/bin/env python3
import sys
import time

def main():
    """
    Simulate a CPU-intensive job
    Usage: python batch_job.py <duration>
    """
    if len(sys.argv) != 2:
        print("Usage: python batch_job.py <duration>")
        sys.exit(1)
    
    try:
        duration = float(sys.argv[1])
    except ValueError:
        print("Error: Duration must be a number")
        sys.exit(1)
    
    # Simulate CPU-intensive work
    start_time = time.time()
    while time.time() - start_time < duration:
        # Perform some CPU-intensive calculations
        _ = sum(i * i for i in range(1000))
    
    print(f"Job completed in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()