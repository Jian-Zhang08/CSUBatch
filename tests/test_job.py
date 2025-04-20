# tests/test_job.py
import unittest
import time
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.job import Job

class TestJob(unittest.TestCase):
    def test_job_initialization(self):
        """Test that a job is initialized with correct values"""
        job = Job("test_job", 5.0, 3)
        self.assertEqual(job.name, "test_job")
        self.assertEqual(job.exec_time, 5.0)
        self.assertEqual(job.priority, 3)
        self.assertEqual(job.status, "Waiting")
        self.assertIsNone(job.arrival_time)
        self.assertIsNone(job.start_time)
        self.assertIsNone(job.end_time)
    
    def test_response_time(self):
        """Test that response time is calculated correctly"""
        job = Job("test_job", 5.0)
        job.arrival_time = time.time()
        time.sleep(0.1)  # Small delay
        job.end_time = time.time()
        
        # Response time should be approximately the time elapsed
        self.assertAlmostEqual(job.get_response_time(), job.end_time - job.arrival_time, places=2)
    
    def test_waiting_time(self):
        """Test that waiting time is calculated correctly"""
        job = Job("test_job", 5.0)
        job.arrival_time = time.time()
        time.sleep(0.1)  # Small delay
        job.start_time = time.time()
        
        # Waiting time should be approximately the time elapsed
        self.assertAlmostEqual(job.get_waiting_time(), job.start_time - job.arrival_time, places=2)
    
    def test_incomplete_job(self):
        """Test that incomplete jobs return None for response time"""
        job = Job("test_job", 5.0)
        job.arrival_time = time.time()
        self.assertIsNone(job.get_response_time())
        
        job.start_time = time.time()
        self.assertIsNone(job.get_response_time())

if __name__ == '__main__':
    unittest.main()