
import sys
import os
import time
import json
from datetime import datetime
import argparse
import threading

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.job import Job
from src.queueManager import JobQueue
from src.scheduler import Scheduler
from src.dispatcher import Dispatcher

# Add this function for the UI to call
def run_performance_test():
    """
    Function to be called from the UI to run performance tests
    """
    print("\nRunning automated performance tests...")
    runner = PerformanceTestRunner()
    runner.run_all_tests()
    print("\nPerformance tests completed.")

class PerformanceTestRunner:
    def __init__(self):
        """Initialize the performance test runner"""
        self.results = {}
        self.test_configs = []
    
    def configure_tests(self):
        """
        Configure the test scenarios to run
        """
        # We'll use the same set of hardcoded jobs for all policies
        policies = ["FCFS", "SJF", "Priority"]
        
        # Create simple test configurations for each policy
        for policy in policies:
            self.test_configs.append({
                "name": f"{policy}_standard_test",
                "policy": policy,
                "test_type": "policy_comparison"
            })
        
        print(f"Configured {len(self.test_configs)} test scenarios")
    
    def create_test_jobs(self):
        """
        Create a predefined set of test jobs with various priorities and execution times
        
        Returns:
            List of job specifications (name, exec_time, priority)
        """

        return [
            ("job_1", 5.0, 1),    
            ("job_2", 0.5, 3),    
            ("job_3", 8.0, 2),    
            ("job_4", 1.0, 5),    
            ("job_5", 3.0, 4),   
            ("job_6", 0.3, 1),   
            ("job_7", 7.0, 2),   
            ("job_8", 0.8, 3),   
            ("job_9", 6.0, 1),    
            ("job_10", 1.5, 4)    
        ]
    
    def run_single_test(self, config):
        """
        Run a single performance test with the given configuration
        
        Args:
            config: Dictionary with test configuration
            
        Returns:
            Dictionary with test results
        """
        print(f"\nRunning test: {config['name']}")
        

        test_jobs = self.create_test_jobs()
        num_jobs = len(test_jobs)
        
        print(f"Total jobs to process: {num_jobs}")
        
        # Create job tracking variables
        job_execution_order = []
        response_times = []
        start_time = time.time()
        
        # Set policy
        print(f"\nUsing {config['policy']} scheduling policy")
        
        # Create a custom queue with all jobs
        job_objects = []
        for i, (name, exec_time, priority) in enumerate(test_jobs):
         
            job = Job(name, exec_time, priority)
            job.arrival_time = start_time + (i * 0.1) 
            job_objects.append(job)
            print(f"Added job: {name} (exec_time: {exec_time}s, priority: {priority})")
        
        # Sort jobs based on the policy
        if config["policy"] == "FCFS":
          
            job_objects.sort(key=lambda j: j.arrival_time)
            print("Jobs sorted by arrival time (FCFS)")
        elif config["policy"] == "SJF":
            
            job_objects.sort(key=lambda j: j.exec_time)
            print("Jobs sorted by execution time (SJF)")
        elif config["policy"] == "Priority":
            
            job_objects.sort(key=lambda j: j.priority, reverse=True)
            print("Jobs sorted by priority (Priority)")
        
        # Print the expected execution order
        expected_order = [job.name for job in job_objects]
        print(f"Expected execution order: {' -> '.join(expected_order)}")
        
        # Process jobs sequentially
        print("\nProcessing jobs sequentially (one at a time):")
        current_time = start_time
        
        for job in job_objects:
            # Update job start time
            job.status = "Running"
            wait_time = max(0, current_time - job.arrival_time)
            job.start_time = current_time
            
            print(f"  Started: {job.name} (waited: {wait_time:.2f}s)")
            job_execution_order.append(job.name)
            
           
            simulation_time = job.exec_time * 0.3
            time.sleep(simulation_time)
            
            # Update current time and completion
            current_time += simulation_time
            job.status = "Completed"
            job.end_time = current_time
            
            # Calculate response time
            response_time = job.end_time - job.arrival_time
            response_times.append(response_time)
            
            print(f"  Completed: {job.name} (response time: {response_time:.2f}s)")
        
       
        test_duration = current_time - start_time
        avg_response_time = sum(response_times) / len(response_times)
        throughput = num_jobs / test_duration
        
     
        results = {
            "name": config["name"],
            "policy": config["policy"],
            "num_jobs": num_jobs,
            "avg_response_time": avg_response_time,
            "throughput": throughput,
            "test_duration": test_duration,
            "timestamp": datetime.now().isoformat(),
            "test_type": config["test_type"],
            "execution_order": job_execution_order,
            "response_times": response_times
        }
        
        print(f"\nTest completed: Avg Response Time: {avg_response_time:.2f}s, Throughput: {throughput:.2f} jobs/s")
        print(f"Job execution order: {' -> '.join(job_execution_order)}")
        
        return results
    
    def run_all_tests(self):
        """
        Run all configured tests and collect results
        """
        if not self.test_configs:
            self.configure_tests()
        
        start_time = time.time()
        print(f"Starting performance tests at {datetime.now().isoformat()}")
        print("Using hardcoded jobs with different priorities and execution times")
        
        all_results = []
        
        for config in self.test_configs:
            results = self.run_single_test(config)
            all_results.append(results)
        
   
        self.results = {
            "policy_comparison": all_results
        }
        
        # Compare results
        self.compare_policies()
        
        # Save results to file
        self.save_results()
        
        end_time = time.time()
        print(f"All tests completed in {end_time - start_time:.2f} seconds")
    
    def compare_policies(self):
        """
        Compare the performance of different policies
        """
        if "policy_comparison" not in self.results or not self.results["policy_comparison"]:
            return
        
        print("\n=== POLICY COMPARISON RESULTS ===")
        
        policy_results = {}
        for result in self.results["policy_comparison"]:
            policy = result["policy"]
            policy_results[policy] = result
        
        print("\nAverage Response Time (lower is better):")
        for policy, result in policy_results.items():
            print(f"  {policy}: {result['avg_response_time']:.2f}s")
        
        print("\nThroughput (higher is better):")
        for policy, result in policy_results.items():
            print(f"  {policy}: {result['throughput']:.2f} jobs/s")
        
        print("\nExecution Order by Policy:")
        for policy, result in policy_results.items():
            print(f"  {policy}: {' -> '.join(result['execution_order'])}")
        
        # Find best policy for each metric
        best_response = min(policy_results.keys(), key=lambda p: policy_results[p]['avg_response_time'])
        best_throughput = max(policy_results.keys(), key=lambda p: policy_results[p]['throughput'])
        
        print("\nBest Performing Policies:")
        print(f"  For Response Time: {best_response}")
        print(f"  For Throughput: {best_throughput}")
        
    
    def save_results(self, filename=None):
        """
        Save test results to a JSON file
        
        Args:
            filename: Optional filename to save results to
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"performance_results_{timestamp}.json"
        
        # Create results directory if it doesn't exist
        results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        file_path = os.path.join(results_dir, filename)
        
        with open(file_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"Results saved to {file_path}")

def main():
    """
    Main entry point for the performance test runner
    """
    parser = argparse.ArgumentParser(description='Run CSUbatch performance tests with hardcoded jobs')
    
    args = parser.parse_args()
    
    runner = PerformanceTestRunner()
    runner.run_all_tests()

if __name__ == "__main__":
    main()