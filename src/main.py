# src/main.py
import time
import threading
from .queueManager import JobQueue
from .scheduler import Scheduler
from .dispatcher import Dispatcher
from .ui import CSUbatchUI

def main():
    """
    Main entry point for the CSUbatch system
    """
    # Create shared job queue
    job_queue = JobQueue()
    
    # Create scheduler and dispatcher threads
    scheduler = Scheduler(job_queue)
    dispatcher = Dispatcher(job_queue, scheduler)
    
    # Create UI
    ui = CSUbatchUI(scheduler, dispatcher, job_queue)
    
    # Set start time for performance measurement
    scheduler.start_time = time.time()
    
    # Start threads
    scheduler.start()
    dispatcher.start()
    
    try:
        # Start UI (blocking)
        ui.cmdloop()
    except KeyboardInterrupt:
        # Handle Ctrl+C
        print("\nShutting down CSUbatch...")
    finally:
        # Stop threads
        scheduler.stop()
        dispatcher.stop()
        
        # Wait for threads to finish
        scheduler.join()
        dispatcher.join()

if __name__ == "__main__":
    main()