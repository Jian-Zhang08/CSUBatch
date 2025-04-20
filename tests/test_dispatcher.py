# tests/test_dispatcher.py
import unittest
import time
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.job import Job
from src.queueManager import JobQueue
from src.scheduler import Scheduler
from src.dispatcher import Dispatcher

class TestDispatcher(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.job_queue = JobQueue()
        self.scheduler = Scheduler(self.job_queue)
        self.dispatcher = Dispatcher(self.job_queue, self.scheduler)
    
    def test_current_job(self):
        """Test getting the current job"""
        # Initially no current job
        self.assertIsNone(self.dispatcher.get_current_job())
        
        # Need to run the dispatcher to test more functionality
        # This would require integration testing
    
    def test_execute_job(self):
        """Test executing a job (mock test)"""
        job = Job("test_job", 0.1)  # Very short job
        
        # Mock the job execution to avoid running the actual process
        original_execute = self.dispatcher.execute_job
        
        def mock_execute(job):
            job.status = "Running"
            job.start_time = time.time()
            time.sleep(job.exec_time)  # Sleep for the job's execution time
            job.status = "Completed"
            job.end_time = time.time()
        
        try:
            self.dispatcher.execute_job = mock_execute
            
            # Execute the job
            self.dispatcher.execute_job(job)
            
            # Check job status after execution
            self.assertEqual(job.status, "Completed")
            self.assertIsNotNone(job.start_time)
            self.assertIsNotNone(job.end_time)
            
            # Check actual execution time
            actual_time = job.end_time - job.start_time
            self.assertAlmostEqual(actual_time, job.exec_time, delta=0.05)
            
        finally:
            # Restore original method
            self.dispatcher.execute_job = original_execute

if __name__ == '__main__':
    unittest.main()