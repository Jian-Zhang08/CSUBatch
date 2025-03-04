# src/job.py
import time

class Job:
    def __init__(self, name, exec_time, priority=0):
        """
        Initialize a new job
        
        Args:
            name (str): Name of the job
            exec_time (float): Execution time in seconds
            priority (int): Priority level (higher number = higher priority)
        """
        self.name = name
        self.exec_time = exec_time
        self.priority = priority
        self.arrival_time = None  # Will be set when job is submitted
        self.start_time = None    # Will be set when job starts execution
        self.end_time = None      # Will be set when job completes
        self.status = "Waiting"   # Current status (Waiting, Running, Completed)
    
    def get_response_time(self):
        """
        Get the response time (turnaround time) of the job
        
        Returns:
            Response time in seconds or None if job hasn't completed
        """
        if self.end_time is not None and self.arrival_time is not None:
            return self.end_time - self.arrival_time
        return None
    
    def get_waiting_time(self):
        """
        Get the waiting time of the job
        
        Returns:
            Waiting time in seconds or None if job hasn't started
        """
        if self.start_time is not None and self.arrival_time is not None:
            return self.start_time - self.arrival_time
        return None