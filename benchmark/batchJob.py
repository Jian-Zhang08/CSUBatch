# benchmark/batch_job.py
import sys
import time

def main():
    # Check if execution time was provided
    if len(sys.argv) < 2:
        print("Usage: python batch_job.py <execution_time_in_seconds>")
        return
    
    try:
        # Parse execution time
        exec_time = float(sys.argv[1])
        
        # Simply sleep for the specified amount of time
        # This simulates a job running without consuming CPU resources
        time.sleep(exec_time)
        
        # Optionally, you can write output to a file instead of terminal
        # with open(f"job_output_{time.time()}.txt", "w") as f:
        #     f.write(f"Job completed after {exec_time} seconds\n")
        
    except ValueError:
        print("Error: Execution time must be a number")

if __name__ == "__main__":
    main()