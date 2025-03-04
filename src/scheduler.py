# src/scheduler.py
import threading
import time
from .job import Job

class Scheduler(threading.Thread):
    def __init__(self, job_queue):
        """
        Initialize the scheduler thread
        
        Args:
            job_queue: The shared job queue
        """
        super().__init__()
        self.job_queue = job_queue
        self.running = True
        self.stats = {
            "total_jobs": 0,
            "completed_jobs": 0,
            "total_response_time": 0,
            "policies": {
                "FCFS": {"jobs": 0, "response_time": 0},
                "SJF": {"jobs": 0, "response_time": 0},
                "Priority": {"jobs": 0, "response_time": 0}
            }
        }
    
    def run(self):
        """
        Main loop for the scheduler thread
        """
        while self.running:
            
            time.sleep(0.1)
            
   
    
    def submit_job(self, name, exec_time, priority=0):
        """
        Submit a new job to the queue
        
        Args:
            name (str): Name of the job
            exec_time (float): Execution time in seconds
            priority (int): Priority level (higher number = higher priority)
        
        Returns:
            The created job object
        """
    
        job = Job(name, exec_time, priority)
        
     
        self.job_queue.add_job(job)
        
       
        self.stats["total_jobs"] += 1
        
        return job
    
    def change_policy(self, policy):
        """
        Change the scheduling policy
        
        Args:
            policy (str): The scheduling policy to use
        """
        if policy in ["FCFS", "SJF", "Priority"]:
          
            self.job_queue.reorder_queue(policy)
            return True
        return False
    
    def register_job_completion(self, job):
        """
        Register that a job has completed
        
        Args:
            job: The completed job
        """
    
        self.stats["completed_jobs"] += 1
        response_time = job.get_response_time()
        if response_time is not None:
            self.stats["total_response_time"] += response_time
            
           
            current_policy = self.job_queue.get_current_policy()
            self.stats["policies"][current_policy]["jobs"] += 1
            self.stats["policies"][current_policy]["response_time"] += response_time
    
    def stop(self):
        """
        Stop the scheduler thread
        """
        self.running = False
    
    def get_performance_stats(self):
        """
        Get the current performance statistics
        
        Returns:
            Dictionary with performance statistics
        """
        stats = self.stats.copy()
        
        # Calculate average response time
        if stats["completed_jobs"] > 0:
            stats["avg_response_time"] = stats["total_response_time"] / stats["completed_jobs"]
        else:
            stats["avg_response_time"] = 0
            
       
        for policy in stats["policies"]:
            if stats["policies"][policy]["jobs"] > 0:
                stats["policies"][policy]["avg_response_time"] = (
                    stats["policies"][policy]["response_time"] / 
                    stats["policies"][policy]["jobs"]
                )
            else:
                stats["policies"][policy]["avg_response_time"] = 0
                
       
        elapsed_time = time.time() - self.start_time if hasattr(self, 'start_time') else 0
        if elapsed_time > 0:
            stats["throughput"] = stats["completed_jobs"] / elapsed_time
        else:
            stats["throughput"] = 0
            
        return stats