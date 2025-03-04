
import threading
import time
from collections import deque

class JobQueue:
    def __init__(self, max_size=float('inf')):
        """
        Initialize the job queue with synchronization primitives
        
        Args:
            max_size (int): Maximum size of the queue
        """
        self.queue = deque()
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)
        self.current_policy = "FCFS"  # Default policy
        self.max_size = max_size
    
    def add_job(self, job):
        """
        Add a job to the queue (producer operation)
        
        Args:
            job: The job to be added
        """
        with self.not_full:
            while len(self.queue) >= self.max_size:

                self.not_full.wait()
            
 
            job.arrival_time = time.time()
            
  
            self.queue.append(job)
 
            self.not_empty.notify()
    
    def get_job(self):
        """
        Get the next job from the queue according to the current policy (consumer operation)
        
        Returns:
            The next job or None if queue is empty
        """
        with self.not_empty:
            while len(self.queue) == 0:
        
                self.not_empty.wait()
            
    
            job = self.queue.popleft()
            
    
            self.not_full.notify()
            
            return job
    
    def reorder_queue(self, policy):
        """
        Reorder the queue according to the given policy
        
        Args:
            policy (str): The scheduling policy to use
        """
        with self.mutex:

            self.current_policy = policy
            

            jobs = list(self.queue)
            

            if policy == "FCFS":
                jobs.sort(key=lambda job: job.arrival_time)
            elif policy == "SJF":
                jobs.sort(key=lambda job: job.exec_time)
            elif policy == "Priority":
                jobs.sort(key=lambda job: job.priority, reverse=True)
            
            self.queue = deque(jobs)
    
    def get_job_list(self):
        """
        Get a list of all jobs in the queue
        
        Returns:
            List of jobs
        """
        with self.mutex:
            return list(self.queue)
    
    def get_queue_size(self):
        """
        Get the current size of the queue
        
        Returns:
            Number of jobs in the queue
        """
        with self.mutex:
            return len(self.queue)
    
    def get_current_policy(self):
        """
        Get the current scheduling policy
        
        Returns:
            Current policy name
        """
        with self.mutex:
            return self.current_policy