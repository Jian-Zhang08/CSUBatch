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