# CSUbatch

CSUbatch is a batch scheduling system that allows users to submit and manage jobs with different scheduling policies (FCFS, SJF, Priority).

## Description

CSUbatch provides a command-line interface for submitting jobs, monitoring their execution, and analyzing performance statistics. It simulates different scheduling algorithms commonly used in batch processing systems.

Key features:
* Submit jobs with execution time and priority parameters
* Change scheduling policy on-the-fly (FCFS, SJF, Priority)
* View job queue and current execution status
* Automated performance testing
* Comprehensive performance statistics

## Getting Started

### Installation Options

#### 1. Standalone Executable (Easiest, No Dependencies)

We provide standalone executables that don't require Python or any dependencies:

**For Windows users:**
1. Download the latest Windows release from the [Releases page](https://github.com/yourusername/CSUbatch/releases)
2. Extract the ZIP file
3. Run `CSUbatch.exe`

**For Linux users:**
1. Download the latest Linux release from the [Releases page](https://github.com/yourusername/CSUbatch/releases)
2. Extract the archive: `tar -xzf CSUbatch-linux.tar.gz`
3. Make the executable file executable if needed: `chmod +x CSUbatch`
4. Run the executable: `./CSUbatch`

That's it! No installation required.

**To build the executable yourself:**

Windows:
```bash
# Clone the repository
git clone https://github.com/yourusername/CSUbatch.git
cd CSUbatch

# Run the build script
.\build_executable.bat
```

Linux:
```bash
# Clone the repository
git clone https://github.com/yourusername/CSUbatch.git
cd CSUbatch

# Make the build script executable
chmod +x build_executable.sh

# Run the build script
./build_executable.sh
```

The executable will be created in the `dist` directory.

#### 2. Running directly from the codebase

```bash
git clone https://github.com/yourusername/CSUbatch.git
cd CSUbatch

python -m src.main 

or

cd src
python main.py
```

#### 3. Using pip

requirements: 
- Install pip for python 3.6: 
- Consider upgrading to a newer Python version

```bash
# Clone the repository
git clone https://github.com/yateeshbalaji/CSUbatch.git
cd CSUbatch

# Install the package
pip install .
```

#### 4. Using Docker (Recommended for Linux)

This is the easiest way to run CSUbatch without installing any dependencies:

```bash
# Clone the repository
git clone https://github.com/yourusername/CSUbatch.git
cd CSUbatch
```

**For Linux/Mac users:**
```bash
# Make the script executable
chmod +x run-docker.sh

# Run the Docker container
./run-docker.sh
```

**For Windows users:**
```powershell
# Option 1: Run the PowerShell script
.\run-docker.ps1

# Option 2: Run Docker commands directly
docker-compose up --build
```

This will build and start a Docker container with CSUbatch. All results will be saved to the `results` directory.

Requirements:
- Docker
- docker-compose

### Executing program

#### 1. If installed with pip

```bash
# Run CSUbatch from anywhere
csubatch
```

#### 2. Using Docker

```bash
./run-docker.sh
```

#### 3. Manual execution

```bash
# Run from the project root directory
python -m src.main

# Or directly
cd src
python main.py
```

## Usage

### Basic Commands

* `run <job_name> <cpu_time> <priority>` - Submit a job
* `list` - Display the job queue
* `fcfs` - Change scheduling policy to First-Come-First-Served
* `sjf` - Change scheduling policy to Shortest Job First
* `priority` - Change scheduling policy to Priority-based
* `performance` - Run automated performance tests comparing scheduling policies
* `test <benchmark> <policy> <num_jobs> <priority_levels> <min_cpu> <max_cpu>` - Run automated performance test
* `quit` - Exit CSUbatch and display performance statistics
* `help` - Display help information

### Example Session

```
$ csubatch

Welcome to CSUbatch. A batch scheduling system.
Type 'help' to see available commands.

CSUbatch> run job1 5 1
Job job1 was submitted.
Total number of jobs in the queue: 1
Expected waiting time: 0.00 seconds
Scheduling Policy: FCFS

CSUbatch> run job2 3 2
Job job2 was submitted.
Total number of jobs in the queue: 2
Expected waiting time: 5.00 seconds
Scheduling Policy: FCFS

CSUbatch> list
Total number of jobs in the queue: 2
Scheduling Policy: FCFS

Name    CPU_Time    Pri    Arrival_Time        Status
-------------------------------------------------------------------
job1    5.00        1      15:30:45            Run
job2    3.00        2      15:30:50            Waiting

CSUbatch> sjf
Scheduling policy is switched to SJF.

CSUbatch> list
Total number of jobs in the queue: 1
Scheduling Policy: SJF

Name    CPU_Time    Pri    Arrival_Time        Status
-------------------------------------------------------------------
job1    5.00        1      15:30:45            Run
job2    3.00        2      15:30:50            Waiting

CSUbatch> test benchmark1 SJF 10 5 1 5
Running performance test with SJF policy...
Submitting 10 jobs with CPU time between 1.0 and 5.0 seconds...
All 10 jobs submitted. Test running...

Test Results:
  Scheduling Policy: SJF
  Number of Jobs: 10
  Total Time: 25.67 seconds
  Average Response Time: 8.32 seconds
  Throughput: 0.39 jobs per second

CSUbatch> quit

Performance Data:
Total number of jobs submitted: 12
Total number of jobs completed: 12
Average turnaround time: 8.45 seconds
Throughput: 0.35 jobs per second

Scheduling Policy Statistics:
  FCFS:
    Jobs completed: 2
    Average turnaround time: 7.50 seconds
  SJF:
    Jobs completed: 10
    Average turnaround time: 8.32 seconds
  Priority:
    Jobs completed: 0

Thank you for using CSUbatch!
```

## Adapting for Linux

When deploying on Linux systems, ensure you:

1. Set proper permissions for the main script:
```bash
chmod +x src/main.py
```

2. If needed, add a shebang line to the main script:
```python
#!/usr/bin/env python3
```

3. For the benchmark scripts:
```bash
chmod +x benchmark/batch_job.py
```

## Running Tests

The system includes a built-in test facility:

```
CSUbatch> test benchmark1 FCFS 20 1 1 10
```

This will run a test with 20 jobs using the FCFS policy, with CPU times ranging from 1 to 10 seconds.

## Help

If you encounter any problems, use the built-in help command:
```
CSUbatch> help
```

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

* CSU Operating Systems course
* Modern batch scheduling systems 