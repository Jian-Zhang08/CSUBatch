import time

class Job:
    def __init__(self, name, exec_time, priority=0):
        """
            Initialize a new job
            name: Name of the job
            exec_time : Execution time in seconds
            priority: Priority level (higher number = higher priority)
        """
        self.name = name
        self.exec_time = exec_time
        self.priority = priority
        self.arrival_time = None  
        self.start_time = None   
        self.end_time = None      
        self.status = "Waiting"   
    
    def get_response_time(self):
        """
        Get the response time of the job
        
        """
        if self.end_time is not None and self.arrival_time is not None:
            return self.end_time - self.arrival_time
        return None
    
    def get_waiting_time(self):
        """
        Get the waiting time of the job
        """
        if self.start_time is not None and self.arrival_time is not None:
            return self.start_time - self.arrival_time
        return None