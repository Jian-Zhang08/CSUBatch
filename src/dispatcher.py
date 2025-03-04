# src/dispatcher.py
import threading
import time
import subprocess
import os
import sys

class Dispatcher(threading.Thread):
    def __init__(self, job_queue, scheduler):
        """
        Initialize the dispatcher thread
        
        Args:
            job_queue: The shared job queue
            scheduler: Reference to the scheduler for reporting job completion
        """
        super().__init__()
        self.job_queue = job_queue
        self.scheduler = scheduler
        self.running = True
        self.current_job = None
    
    def run(self):
        """
        Main loop for the dispatcher thread
        """
        while self.running:
            # Get next job from queue
            try:
                job = self.job_queue.get_job()
                self.current_job = job
                
                job.status = "Running"
                job.start_time = time.time()
   
                print(f"Executing job: {job.name} (expected time: {job.exec_time} seconds)")
                self.execute_job(job)
        
                job.status = "Completed"
                job.end_time = time.time()
                
                
                actual_exec_time = job.end_time - job.start_time
                print(f"Job completed: {job.name} (actual time: {actual_exec_time:.2f} seconds)")
                
               
                self.scheduler.register_job_completion(job)
                
                self.current_job = None
                
            except Exception as e:
                print(f"Error in dispatcher: {e}")
                time.sleep(1)  # Wait a bit before retrying
    
    def execute_job(self, job):
        """
        Execute a job
        
        Args:
            job: The job to execute
        """
        try:
            # Get the path to the benchmark script
            # Use relative path from the current file's location
            current_dir = os.path.dirname(os.path.abspath(__file__))
            script_path = os.path.join(os.path.dirname(current_dir), "benchmark", "batch_job.py")
            
            # Run the benchmark script with the job's execution time
            subprocess.run([sys.executable, script_path, str(job.exec_time)], 
                          check=True)
            
        except subprocess.CalledProcessError as e:
            print(f"Error executing job {job.name}: {e}")
    
    def stop(self):
        """
        Stop the dispatcher thread
        """
        self.running = False
    
    def get_current_job(self):
        """
        Get the currently running job
        
        Returns:
            The currently running job or None
        """
        return self.current_job