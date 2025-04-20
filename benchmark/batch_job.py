import sys
import time

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_job.py <execution_time_in_seconds>")
        return
    
    try:
        exec_time = float(sys.argv[1])
        # This simulates a job running without consuming CPU resources
        time.sleep(exec_time)
        
    except ValueError:
        print("Error: Execution time must be a number")

if __name__ == "__main__":
    main()