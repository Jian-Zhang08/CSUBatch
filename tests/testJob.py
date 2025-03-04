# tests/test_performance.py
import sys
import os
import time
import random
import subprocess
import matplotlib.pyplot as plt
import numpy as np

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from job import Job
from queue_manager import JobQueue
from scheduler import Scheduler
from dispatcher import Dispatcher

def run_test(policy, num_jobs, min_cpu, max_cpu, priority_levels=1, arrival_rate=0.5):
    """
    Run a performance test with the given parameters
    
    Args:
        policy (str): Scheduling policy to use
        num_jobs (int): Number of jobs to submit
        min_cpu (float): Minimum CPU time
        max_cpu (float): Maximum CPU time
        priority_levels (int): Number of priority levels
        arrival_rate (float): Job arrival rate (jobs per second)
    
    Returns:
        Dictionary with performance metrics
    """
    # Create shared job queue
    job_queue = JobQueue()
    
    # Create scheduler and dispatcher threads
    scheduler = Scheduler(job_queue)
    dispatcher = Dispatcher(job_queue, scheduler)
    
    # Set start time for performance measurement
    scheduler.start_time = time.time()
    
    # Start threads
    scheduler.start()
    dispatcher.start()
    
    # Set scheduling policy
    scheduler.change_policy(policy)
    
    # Submit jobs
    for i in range(num_jobs):
        # Generate random CPU time
        cpu_time = min_cpu + random.random() * (max_cpu - min_cpu)
        
        # Generate random priority
        priority = random.randint(1, priority_levels) if policy == "Priority" else 0
        
        # Submit job
        job_name = f"test_job_{i+1}"
        scheduler.submit_job(job_name, cpu_time, priority)
        
        # Sleep according to arrival rate
        if i < num_jobs - 1:  # No need to sleep after the last job
            time.sleep(1.0 / arrival_rate)
    
    # Wait for all jobs to complete
    while scheduler.stats["completed_jobs"] < num_jobs:
        time.sleep(0.1)
    
    # Get performance statistics
    stats = scheduler.get_performance_stats()
    
    # Stop threads
    scheduler.stop()
    dispatcher.stop()
    
    # Wait for threads to finish
    scheduler.join()
    dispatcher.join()
    
    return stats

def run_all_tests():
    """
    Run performance tests with different configurations and plot results
    """
    # Test configurations
    policies = ["FCFS", "SJF", "Priority"]
    job_counts = [5, 10, 15, 20, 25]
    arrival_rates = [0.1, 0.2, 0.5, 1.0]
    load_distributions = [
        {"name": "Light [0.1, 0.5]", "min": 0.1, "max": 0.5},
        {"name": "Medium [0.1, 1]", "min": 0.1, "max": 1.0},
        {"name": "Heavy [0.5, 1]", "min": 0.5, "max": 1.0},
        {"name": "Very Heavy [1, 10]", "min": 1.0, "max": 10.0}
    ]
    
    # Results
    results = {}
    
    # Run tests with varying job counts
    print("Running tests with varying job counts...")
    for policy in policies:
        results[f"{policy}_job_counts"] = []
        for count in job_counts:
            print(f"  Testing {policy} with {count} jobs...")
            stats = run_test(
                policy=policy,
                num_jobs=count,
                min_cpu=0.1,
                max_cpu=1.0,
                priority_levels=3,
                arrival_rate=0.5
            )
            results[f"{policy}_job_counts"].append(stats["avg_response_time"])
    
    # Run tests with varying arrival rates
    print("Running tests with varying arrival rates...")
    for policy in policies:
        results[f"{policy}_arrival_rates"] = []
        for rate in arrival_rates:
            print(f"  Testing {policy} with arrival rate {rate}...")
            stats = run_test(
                policy=policy,
                num_jobs=15,
                min_cpu=0.1,
                max_cpu=1.0,
                priority_levels=3,
                arrival_rate=rate
            )
            results[f"{policy}_arrival_rates"].append(stats["avg_response_time"])
    
    # Run tests with varying load distributions
    print("Running tests with varying load distributions...")
    for policy in policies:
        results[f"{policy}_load_distributions"] = []
        for dist in load_distributions:
            print(f"  Testing {policy} with load distribution {dist['name']}...")
            stats = run_test(
                policy=policy,
                num_jobs=15,
                min_cpu=dist["min"],
                max_cpu=dist["max"],
                priority_levels=3,
                arrival_rate=0.5
            )
            results[f"{policy}_load_distributions"].append(stats["avg_response_time"])
    
    # Plot results
    # Job count variation
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    for policy in policies:
        plt.plot(job_counts, results[f"{policy}_job_counts"], marker='o', label=policy)
    plt.xlabel('Number of Jobs')
    plt.ylabel('Avg. Response Time (s)')
    plt.title('Response Time vs. Number of Jobs')
    plt.legend()
    plt.grid(True)
    
    # Arrival rate variation
    plt.subplot(3, 1, 2)
    for policy in policies:
        plt.plot(arrival_rates, results[f"{policy}_arrival_rates"], marker='o', label=policy)
    plt.xlabel('Arrival Rate (jobs/sec)')
    plt.ylabel('Avg. Response Time (s)')
    plt.title('Response Time vs. Arrival Rate')
    plt.legend()
    plt.grid(True)
    
    # Load distribution variation
    plt.subplot(3, 1, 3)
    x = np.arange(len(load_distributions))
    width = 0.25
    for i, policy in enumerate(policies):
        plt.bar(x + i*width, results[f"{policy}_load_distributions"], width, label=policy)
    plt.xlabel('Load Distribution')
    plt.ylabel('Avg. Response Time (s)')
    plt.title('Response Time vs. Load Distribution')
    plt.xticks(x + width, [d["name"] for d in load_distributions], rotation=45)
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('performance_results.png')
    plt.show()

if __name__ == "__main__":
    run_all_tests()