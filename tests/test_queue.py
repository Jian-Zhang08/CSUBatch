# tests/test_queue.py
import unittest
import time
import threading
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.job import Job
from src.queueManager import JobQueue

class TestJobQueue(unittest.TestCase):
    def test_add_get_job(self):
        """Test adding and getting a job from the queue"""
        queue = JobQueue()
        job = Job("test_job", 5.0, 3)
        
        queue.add_job(job)
        self.assertEqual(queue.get_queue_size(), 1)
        
        retrieved_job = queue.get_job()
        self.assertEqual(retrieved_job.name, "test_job")
        self.assertEqual(queue.get_queue_size(), 0)
    
    def test_fcfs_ordering(self):
        """Test that FCFS ordering is maintained"""
        queue = JobQueue()
        queue.reorder_queue("FCFS")
        
        # Create jobs with explicitly set arrival times
        job1 = Job("job1", 5.0)
        job1.arrival_time = time.time()
        time.sleep(0.01)  # Ensure each job has a different arrival time
        
        job2 = Job("job2", 2.0)
        job2.arrival_time = time.time()
        time.sleep(0.01)
        
        job3 = Job("job3", 8.0)
        job3.arrival_time = time.time()
        
        # Add jobs in reverse order
        queue.add_job(job3)
        queue.add_job(job2)
        queue.add_job(job1)
        
        # Print arrival times for debugging
        print(f"job1 arrival: {job1.arrival_time}")
        print(f"job2 arrival: {job2.arrival_time}")
        print(f"job3 arrival: {job3.arrival_time}")
        
        # Reorder to FCFS (by arrival time)
        queue.reorder_queue("FCFS")
        
        # Retrieve jobs - should be in arrival time order
        retrieved1 = queue.get_job()
        retrieved2 = queue.get_job()
        retrieved3 = queue.get_job()
        
        self.assertEqual(retrieved1.name, "job1")
        self.assertEqual(retrieved2.name, "job2")
        self.assertEqual(retrieved3.name, "job3")
    
    def test_sjf_ordering(self):
        """Test that SJF ordering is maintained"""
        queue = JobQueue()
        
        # Add jobs with different execution times
        job1 = Job("job1", 5.0)
        job2 = Job("job2", 2.0)
        job3 = Job("job3", 8.0)
        
        queue.add_job(job1)
        queue.add_job(job2)
        queue.add_job(job3)
        
        # Reorder to SJF
        queue.reorder_queue("SJF")
        
        # Retrieve jobs - should be in execution time order
        retrieved1 = queue.get_job()
        retrieved2 = queue.get_job()
        retrieved3 = queue.get_job()
        
        self.assertEqual(retrieved1.name, "job2")  # 2.0
        self.assertEqual(retrieved2.name, "job1")  # 5.0
        self.assertEqual(retrieved3.name, "job3")  # 8.0
    
    def test_priority_ordering(self):
        """Test that Priority ordering is maintained"""
        queue = JobQueue()
        
        # Add jobs with different priorities
        job1 = Job("job1", 5.0, 2)
        job2 = Job("job2", 2.0, 1)
        job3 = Job("job3", 8.0, 3)
        
        queue.add_job(job1)
        queue.add_job(job2)
        queue.add_job(job3)
        
        # Reorder to Priority (higher priority first)
        queue.reorder_queue("Priority")
        
        # Retrieve jobs - should be in priority order (highest first)
        retrieved1 = queue.get_job()
        retrieved2 = queue.get_job()
        retrieved3 = queue.get_job()
        
        self.assertEqual(retrieved1.name, "job3")  # priority 3
        self.assertEqual(retrieved2.name, "job1")  # priority 2
        self.assertEqual(retrieved3.name, "job2")  # priority 1
    
    def test_synchronization(self):
        """Test that the queue properly handles concurrent access"""
        queue = JobQueue()
        total_jobs = 100
        jobs_processed = []
        
        # Producer thread adds jobs to the queue
        def producer():
            for i in range(total_jobs):
                job = Job(f"job{i}", i/10)
                queue.add_job(job)
                time.sleep(0.001)  # Small delay
        
        # Consumer thread gets jobs from the queue
        def consumer():
            for _ in range(total_jobs):
                job = queue.get_job()
                jobs_processed.append(job.name)
                time.sleep(0.002)  # Small delay
        
        # Start threads
        producer_thread = threading.Thread(target=producer)
        consumer_thread = threading.Thread(target=consumer)
        
        producer_thread.start()
        consumer_thread.start()
        
        # Wait for threads to complete
        producer_thread.join()
        consumer_thread.join()
        
        # Check that all jobs were processed
        self.assertEqual(len(jobs_processed), total_jobs)
        
        # Queue should be empty
        self.assertEqual(queue.get_queue_size(), 0)

if __name__ == '__main__':
    unittest.main()