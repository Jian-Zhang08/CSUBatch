# tests/test_scheduler.py
import unittest
import time
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.job import Job
from src.queueManager import JobQueue
from src.scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.job_queue = JobQueue()
        self.scheduler = Scheduler(self.job_queue)
        self.scheduler.start()
    
    def tearDown(self):
        """Tear down test fixtures"""
        self.scheduler.stop()
        self.scheduler.join()
    
    def test_submit_job(self):
        """Test submitting a job"""
        job = self.scheduler.submit_job("test_job", 5.0, 3)
        
        self.assertEqual(job.name, "test_job")
        self.assertEqual(job.exec_time, 5.0)
        self.assertEqual(job.priority, 3)
        self.assertEqual(self.job_queue.get_queue_size(), 1)
        self.assertEqual(self.scheduler.stats["total_jobs"], 1)
    
    def test_change_policy(self):
        """Test changing the scheduling policy"""
        self.assertTrue(self.scheduler.change_policy("FCFS"))
        self.assertEqual(self.job_queue.get_current_policy(), "FCFS")
        
        self.assertTrue(self.scheduler.change_policy("SJF"))
        self.assertEqual(self.job_queue.get_current_policy(), "SJF")
        
        self.assertTrue(self.scheduler.change_policy("Priority"))
        self.assertEqual(self.job_queue.get_current_policy(), "Priority")
        
        # Invalid policy should return False
        self.assertFalse(self.scheduler.change_policy("INVALID"))
    
    def test_register_job_completion(self):
        """Test registering a completed job"""
        job = Job("test_job", 5.0)
        job.arrival_time = time.time()
        time.sleep(0.1)
        job.end_time = time.time()
        
        self.scheduler.register_job_completion(job)
        
        self.assertEqual(self.scheduler.stats["completed_jobs"], 1)
        self.assertGreater(self.scheduler.stats["total_response_time"], 0)
    
    def test_get_performance_stats(self):
        """Test getting performance statistics"""
        # Submit and complete a job
        job = self.scheduler.submit_job("test_job", 5.0)
        job.arrival_time = time.time()
        time.sleep(0.1)
        job.end_time = time.time()
        
        self.scheduler.register_job_completion(job)
        
        stats = self.scheduler.get_performance_stats()
        
        self.assertEqual(stats["total_jobs"], 1)
        self.assertEqual(stats["completed_jobs"], 1)
        self.assertGreater(stats["avg_response_time"], 0)

if __name__ == '__main__':
    unittest.main()