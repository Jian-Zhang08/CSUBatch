#!/usr/bin/env python3
# src/main.py
import time
import threading
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.queueManager import JobQueue
from src.scheduler import Scheduler
from src.dispatcher import Dispatcher
from src.ui import CSUbatchUI

def main():
    """
    Main entry point for the CSUbatch system
    """
   
    job_queue = JobQueue()
    
 
    scheduler = Scheduler(job_queue)
    dispatcher = Dispatcher(job_queue, scheduler)
    

    ui = CSUbatchUI(scheduler, dispatcher, job_queue)
    

    scheduler.start_time = time.time()
    

    scheduler.start()
    dispatcher.start()
    
    try:

        ui.cmdloop()
    except KeyboardInterrupt:
  
        print("\nShutting down CSUbatch...")
    finally:
 
        scheduler.stop()
        dispatcher.stop()
        
      
        scheduler.join()
        dispatcher.join()

if __name__ == "__main__":
    main()