# src/ui.py
import cmd
import time
import random
from src.job import Job

class CSUbatchUI(cmd.Cmd):
    """Command-line interface for CSUbatch scheduling system"""
    
    prompt = "CSUbatch> "
    intro = """
Welcome to CSUbatch. A batch scheduling system.
Type 'help' to see available commands.
"""

    def __init__(self, scheduler, dispatcher, job_queue):
        """
        Initialize the UI
        
        Args:
            scheduler: The scheduler thread
            dispatcher: The dispatcher thread
            job_queue: The shared job queue
        """
        super().__init__()
        self.scheduler = scheduler
        self.dispatcher = dispatcher
        self.job_queue = job_queue
    
    def do_help(self, arg):
        """
        Show help information
        """
        print("\nCSUbatch Help:")
        print("  run <job_name> <cpu_time> <priority>: Submit a job")
        print("  list: Display the job queue")
        print("  fcfs: Change the scheduling policy to FCFS")
        print("  sjf: Change the scheduling policy to SJF")
        print("  priority: Change the scheduling policy to Priority")
        print("  test <benchmark> <policy> <num_jobs> <priority_levels> <min_cpu> <max_cpu>: "
              "Run automated performance test")
        print("  quit: Exit CSUbatch")
        print("  help: Display this help message\n")
    
    def do_run(self, arg):
        """
        Submit a job
        
        Format: run <job_name> <cpu_time> <priority>
        """
        args = arg.split()
        if len(args) < 2:
            print("Error: Missing parameters")
            print("Usage: run <job_name> <cpu_time> [priority]")
            return
        
        try:
            job_name = args[0]
            cpu_time = float(args[1])
            priority = int(args[2]) if len(args) > 2 else 0
           
            job = self.scheduler.submit_job(job_name, cpu_time, priority)
            
           
            queue_size = self.job_queue.get_queue_size()
            policy = self.job_queue.get_current_policy()
            
            print(f"\nJob {job_name} was submitted.")
            print(f"Total number of jobs in the queue: {queue_size}")
            print(f"Expected waiting time: {self._calculate_expected_waiting_time(job):.2f} seconds")
            print(f"Scheduling Policy: {policy}\n")
            
        except ValueError:
            print("Error: Invalid parameters")
            print("Usage: run <job_name> <cpu_time> [priority]")
    
    def do_list(self, arg):
        """
        Display the job queue
        """
        jobs = self.job_queue.get_job_list()
        queue_size = len(jobs)
        policy = self.job_queue.get_current_policy()
        
        print(f"\nTotal number of jobs in the queue: {queue_size}")
        print(f"Scheduling Policy: {policy}")
        
        if queue_size > 0:
            print("\nName\tCPU_Time\tPri\tArrival_Time\t\tStatus")
            print("-------------------------------------------------------------------")
            
           
            current_job = self.dispatcher.get_current_job()
            
            
            if current_job:
                self._print_job_info(current_job, is_running=True)
                
           
            for job in jobs:
                self._print_job_info(job)
            
        print("")
    
    def do_fcfs(self, arg):
        """
        Change the scheduling policy to FCFS
        """
        self.scheduler.change_policy("FCFS")
        print("\nScheduling policy is switched to FCFS.\n")
    
    def do_sjf(self, arg):
        """
        Change the scheduling policy to SJF
        """
        self.scheduler.change_policy("SJF")
        print("\nScheduling policy is switched to SJF.\n")
    
    def do_priority(self, arg):
        """
        Change the scheduling policy to Priority
        """
        self.scheduler.change_policy("Priority")
        print("\nScheduling policy is switched to Priority.\n")
    
    def do_test(self, arg):
        """
        Run automated performance test
        
        Format: test <benchmark> <policy> <num_jobs> <priority_levels> <min_cpu> <max_cpu>
        """
        args = arg.split()
        if len(args) < 6:
            print("Error: Missing parameters")
            print("Usage: test <benchmark> <policy> <num_jobs> <priority_levels> <min_cpu> <max_cpu>")
            return
        
        try:
            benchmark = args[0]
            policy = args[1]
            num_jobs = int(args[2])
            priority_levels = int(args[3])
            min_cpu = float(args[4])
            max_cpu = float(args[5])
            
            if policy not in ["FCFS", "SJF", "Priority"]:
                print(f"Error: Unknown policy '{policy}'")
                return
            
            # Change policy
            self.scheduler.change_policy(policy)
            
            print(f"\nRunning performance test with {policy} policy...")
            print(f"Submitting {num_jobs} jobs with CPU time between {min_cpu} and {max_cpu} seconds...")
            
            start_time = time.time()
            
            # Submit jobs
            for i in range(num_jobs):
                # Generate random CPU time
                cpu_time = min_cpu + random.random() * (max_cpu - min_cpu)
                
                # Generate random priority
                priority = random.randint(1, priority_levels) if policy == "Priority" else 0
                
                # Submit job
                job_name = f"{benchmark}_{i+1}"
                self.scheduler.submit_job(job_name, cpu_time, priority)
                
                # Sleep briefly to avoid overwhelming the system
                time.sleep(0.01)
            
            print(f"All {num_jobs} jobs submitted. Test running...")
            
            # Wait for jobs to complete
            while self.scheduler.stats["completed_jobs"] < num_jobs:
                time.sleep(0.1)
            
            # Calculate test results
            elapsed_time = time.time() - start_time
            stats = self.scheduler.get_performance_stats()
            throughput = num_jobs / elapsed_time
            
            print("\nTest Results:")
            print(f"  Scheduling Policy: {policy}")
            print(f"  Number of Jobs: {num_jobs}")
            print(f"  Total Time: {elapsed_time:.2f} seconds")
            print(f"  Average Response Time: {stats['avg_response_time']:.2f} seconds")
            print(f"  Throughput: {throughput:.2f} jobs per second\n")
            
        except ValueError:
            print("Error: Invalid parameters")
            print("Usage: test <benchmark> <policy> <num_jobs> <priority_levels> <min_cpu> <max_cpu>")
    
    def do_quit(self, arg):
        """
        Exit CSUbatch and display performance statistics
        """
        
        stats = self.scheduler.get_performance_stats()
        
        print("\nPerformance Data:")
        print(f"Total number of jobs submitted: {stats['total_jobs']}")
        print(f"Total number of jobs completed: {stats['completed_jobs']}")
        
        if stats['completed_jobs'] > 0:
            print(f"Average turnaround time: {stats['avg_response_time']:.2f} seconds")
            print(f"Throughput: {stats['throughput']:.2f} jobs per second")
            
            print("\nScheduling Policy Statistics:")
            for policy in ["FCFS", "SJF", "Priority"]:
                policy_stats = stats['policies'][policy]
                if policy_stats['jobs'] > 0:
                    print(f"  {policy}:")
                    print(f"    Jobs completed: {policy_stats['jobs']}")
                    print(f"    Average turnaround time: {policy_stats['avg_response_time']:.2f} seconds")
        
        print("\nThank you for using CSUbatch!\n")
        
        # Stop threads
        self.scheduler.stop()
        self.dispatcher.stop()
        
        return True
    
    def _calculate_expected_waiting_time(self, job):
        """
        Calculate the expected waiting time for a job
        
        Args:
            job: The job to calculate waiting time for
            
        Returns:
            Expected waiting time in seconds
        """
     
        jobs = self.job_queue.get_job_list()
        
        
        policy = self.job_queue.get_current_policy()
        
        waiting_time = 0
        
        
        current_job = self.dispatcher.get_current_job()
        if current_job:
           
            elapsed = time.time() - current_job.start_time
            remaining = max(0, current_job.exec_time - elapsed)
            waiting_time += remaining
        
       
        for queue_job in jobs:
            if policy == "FCFS" and queue_job.arrival_time <= job.arrival_time:
                waiting_time += queue_job.exec_time
            elif policy == "SJF" and queue_job.exec_time <= job.exec_time:
                waiting_time += queue_job.exec_time
            elif policy == "Priority" and queue_job.priority >= job.priority:
                waiting_time += queue_job.exec_time
        
        return waiting_time
    
    def _print_job_info(self, job, is_running=False):
        """
        Print job information
        
        Args:
            job: The job to print information for
            is_running: Whether the job is currently running
        """
    
        arrival_time = time.strftime("%H:%M:%S", time.localtime(job.arrival_time)) if job.arrival_time else "N/A"
        

        status = "Run" if is_running else job.status
        
        print(f"{job.name}\t{job.exec_time:.2f}\t\t{job.priority}\t{arrival_time}\t\t{status}")