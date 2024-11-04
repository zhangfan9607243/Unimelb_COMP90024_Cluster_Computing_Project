# Unimelb COMP90024 Cluster Computing Project

## Acknowledgments
Thanks to the Unimelb COMP90024 2023S1 teaching team for providing this project opportunity and to the Unimelb SPARTAN HPC facility for providing computational resources.

## Project Introduction
Nowadays, social network platforms create massive amounts of data every day. It will be a challenge to deal with such a large amount of data. One possible approach is to process the data in parallel.

In this project, we implemented a parallelized application for analyzing Twitter data, utilizing the University of Melbourne's High-Performance Computing (HPC) facility, SPARTAN. 

The main objectives of this assignment are, given a JSON file that contains Tweets and a `sal.json` dictionary that maps suburbs to their corresponding Greater Capital cities, to:
- Task 1: Count the number of different tweets made in the Greater Capital cities of Australia.
- Task 2: Identify the Twitter accounts that have made the most tweets.
- Task 3: Identify the users that have tweeted from the most different Greater Capital cities.

The programming language used is Python, with parallel computing achieved by the `mpi4py` package. The performance of our main parallel method is compared with a baseline method that involves no parallel execution, and two alternative parallel methods that we have tried and proved to perform worse than our main method.

## File Descriptions
The following is a detailed instructions to the files & paths:
* `/data/`:
  * `sal.json`: This file is a map dictionary that contains the suburb names in Australia and which great capital city they belong to.
  * `tinyTwitter.json`: The Twitter data file (1.5Mb).
  * `smallTwitter.json`: The Twitter data file (242Mb).
  * `bigTwitter.json`: The Twitter data file (18.74Gb).
* `/slurm_files/`: The shell file to submit jobs on SPARTAN HPC.
  * `non_parallel.slurm`
  * `parallel_method1_n1c8.slurm`
  * `parallel_method1_n2c8.slurm`
  * `parallel_method2_n1c8.slurm`
  * `parallel_method2_n2c8.slurm`
  * `parallel_method3_n1c8.slurm`
  * `parallel_method3_n2c8.slurm`
* `/slurm_outputs/`: The job output from SPARTAN HPC.
  * `non_parallel.out`
  * `parallel_method1_n1c8.out`
  * `parallel_method1_n2c8.out`
  * `parallel_method2_n1c8.out`
  * `parallel_method2_n2c8.out`
  * `parallel_method3_n1c8.out`
  * `parallel_method3_n2c8.out`
* `/non_parallel.py`: This is the source code of our baseline sequential execution method.
* `/parallel_method1.py`: This is the source code of an alternative parallel method, which reads data by a single core but processes data in parallel.
* `/parallel_method2.py`: This is the source code of an alternative parallel method, which reads data in parallel by a signal for cores.
* `/parallel_method3.py`: This is the source code of our main parallel method, which reads in parallel by splitting the data file.


## Code Instruction
### 1. If You CAN Access Unimelb SPARTAN HPC
#### (1) Data Preparation
In your own SPARTAN user directory, change directory to the `/data/` path of this project. Then, make a symbolic link to these files on SPARTAN through the following commands:
```
ln –s /data/projects/COMP90024/bigTwitter.json
ln –s /data/projects/COMP90024/smallTwitter.json
ln –s /data/projects/COMP90024/tinyTwitter.json
ln –s /data/projects/COMP90024/sal.json
```

Then, these data files will be located in the `/data/` path (although these are symbolic links, they do not affect usage.).

#### (2) Program Execution
There are 7 slurm files in the path `/slurm_files/`, which are shell file to submit jobs on SPARTAN HPC. 

The following shows the contents of the file `parallel_method3_n2c8.slurm`, as an example
```
#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --time=0-01:00:00

module load mpi4py/3.0.2-timed-pingpong
module load python/3.7.4
module load numpy/1.18.0-python-3.7.4

time mpiexec -n 8 python3 parallel_method3.py
my-job-stats -a -n -s
```

In this file:
* `#!/bin/bash`: This indicates that the script should be run using the Bash shell.
* `#SBATCH --nodes=2`: This specifies that the job requires 2 nodes (computers) in the cluster.
* `#SBATCH --ntasks=8`: This indicates that the job will use a total of 8 tasks (processes) across the nodes.
* `#SBATCH --time=0-01:00:00`: This sets a maximum runtime of 1 hour for the job, formatted as days-hours:minutes:seconds
* `module load mpi4py/3.0.2-timed-pingpong`: This loads a specific version of the mpi4py module, which is a Python package for MPI.
* `module load python/3.7.4`: This loads a specific version of Python (3.7.4) to be used for running the script.
* `module load numpy/1.18.0-python-3.7.4`: This loads a specific version of NumPy, a library for numerical computing in Python.
* `time mpiexec -n 8 python3 parallel_method3.py`: This runs the parallel_method3.py script using MPI, with 8 processes, and measures the execution time.
* `my-job-stats -a -n -s`: This command requests that the output includes the task status as well.

Then, to submit jobs on SPARTAN HPC, we should use the following command at SPARTAN login node:
```
$ sbatch myfirstjob.slurm
```

After this command completes, it will submit the job to SPARTAN. The job will first be queued and then run. Once it finishes, a `.out` text file will be returned in the directory where you submitted the job, containing the results of the job execution.

### 2. If You CANNOT Access Unimelb SPARTAN HPC (Run Locally)
#### (1) Data Preparation
First, you can access the data through the following ways.
  * `sal.json`: Already contained in the `/data/` of this repository.
  * `tinyTwitter.json`: Already contained in the `/data/` of this repository.
  * `smallTwitter.json`: Access through the link: https://pan.baidu.com/s/1ZqBevgcc4QxEZgmcLDvnPw?pwd=1234.
  * `bigTwitter.json`: Access through the link: https://pan.baidu.com/s/1ZqBevgcc4QxEZgmcLDvnPw?pwd=1234.

Then, you can put these data files in the `/data/` path of the cloned repository on your local device.

#### (2) Program Execution
First, please ensure that package `mpi4py` is installed in your Python environment.

Then, in the main 3 Python files with parallel programming (`parallel_method1.py`, `parallel_method2.py`, and `parallel_method3.py`), you can specify the name of the Twitter file to run (`tinyTwitter.json`, `smallTwitter.json`, or `bigTwitter.json`). 

Then, you can run the following command in the terminal.

```
$ time mpirun --oversubscribe -np 8 python file_name.py
```

In this command:
* `time`: This command can help you record the runtime.
* `mpirun`: This is the command used to launch MPI (Message Passing Interface) applications.
* `--oversubscribe`: This option allows you to start more processes than there are available slots (or resources) in the system. In other words, even if your system has fewer cores than the number of processes you want to run, it will still allow you to launch them.
* `-np 8`: This option specifies the number of processes to start, which is 8 in this case. You cannot change this number because my program has already specified the tasks for each of the 8 threads.
* `python file_name.py`: This indicates the Python script you want to run. You can choose from `parallel_method1.py`, `parallel_method2.py`, and `parallel_method3.py`.

Note that you don't need to run `non_parallel.py` with the above command; you can simply run it using command `python non_parallel.py`, as this file is not set up for multi-threading.

## Project Report
### 1. Performance Overview
The running time on `bigTwitter.json` of the main parallel method, together with the baseline method and two alternative parallel methods, are presented as below.
<img width="878" alt="截屏2024-11-04 23 30 16" src="https://github.com/user-attachments/assets/088197fe-78e7-4d2c-ae11-64b9634e8cd4">

### 2. Methods
#### (1) Baseline Method: Sequential Execution (non_parallel.py)
The idea of sequential execution is simple. Although it does not involve a parallel mechanism, the sequential execution method provides a basic methodology for solving problems in this task.

Firstly, we read the json files, with the suburb file read entirely due to its small size, and the Twitter file read line by line due to its large size. While reading the Twitter file, we only extract objects that we are interested in: pairs of author id and suburb. Then, we count the number of objects we care about by three Python dictionaries corresponding to the three tasks in this assignment. Finally, when the count is over, we process the dictionaries to produce the summary tables.

For the sequential execution method, it can only run on 1 node 1 core resource, which has a 349.37s running time. The sequential execution method will be used as a foundation. All the other methods are modifications based on the sequential execution method, and their performance will be compared with the sequential execution method.

#### (2) Main Parallel Method: Read in Parallel by Splitting the Data File (parallel_method3.py)
The main parallel method has the best performance when comparing other parallel methods we tried. In this part, we will describe this method step by step.

Firstly, our basic idea is to split the large Twitter file into eight parts, then each core reads one part of the file simultaneously. To implement this idea, we should get the whole file size and divide it into eight parts on average, also we need to get the start and end position of each part. Then for each core, we decide which part of the file it should read. The function `seek()` can be applied to find the start position of the part which should be read in this core, the function `tell()` can help us to determine whether it comes to the end of this part during reading steps. For each core, pairs of author id and its suburb from its file part are collected in a list, then only one core is used to gather all the lists from eight cores.

It is worth noting that, in this reading method, summary statistics may be slightly inaccurate. This is because that when split the Twitter file, it is possible that the split point is exactly between the author ID and the suburb of the same tweet, which makes our algorithm ignore this tweet while reading. However, the decrease in accuracy is negligible, because the maximum number of tweets that is possible to be ignored equals to the number of cores used, which is 8 in this case and is negligible in a Twitter file with millions of tweets.

Then, we do all the subsequent statistics and summary steps, as in sequential execution, in only one core. The reason for not introducing parallel computation in this part is simple. On one hand, data processing mainly involves accessing data in memory, which is significantly faster than accessing data in disk as in the reading procedure. On the other hand, in this case, the data stored in memory is the 3 python dictionaries that we introduced in sequential execution method, which has significantly smaller size that the Twitter file stored in disk. So, in our view, in this part, it is not necessary to process data in parallel.

This method has the best performance, which runs 206.97s on 1 node 8 cores and 83.78s on 2 node 8 cores. Also, we have the same output as the baseline method. For 1 node 8 cores, the time spent by running this parallel method is 60% of the time spent by running the baseline method. For 2 node 8 cores, the percentage is dropped from 60% to 24%. The code speed increases significantly when using this parallel method, which shows that executing reading file steps in parallel has the best performance to increase the code speed. Therefore, we use this parallel method as our main parallel method.

#### (3) Other Parallel Methods 1: Read Data in Parallel by a Signal for Cores (parallel_method2.py)
When we first thought about reading data in parallel, we came up with this method. In this parallel method, all the cores browse the Twitter file but capture objects (pair of author id and suburb) in turn. While browsing the Twitter file, when an object is found, only the core, whose turn it is, captures the object, and all the other cores continuously browse the Twitter file and look for the next object. This can be done by setting a signal suggesting whose turn it is now.

This method does not have a good performance, which runs 525.76s on 1 node 8 cores and 484.07s on 2 node 8 cores, which is even slower than sequential execution, though accelerated by adding nodes. The reason is that, in fact, all the cores have to fully go through the Twitter file, in this method. So, in theory, it cannot be faster than sequential execution. Additionally, compared with single core, when more cores are added, the percentage of usage of a single core will decrease. Therefore, in this case, running in 1 node 8 core has the worst performance.

#### (4) Other Parallel Methods 2: Read Data by a Single Core but Process Data in Parallel (parallel_method1.py)
When we first thought about parallel execution, we came up with this method. In this parallel method, the read of data from json files is completed by a single core. The other 7 cores are responsible for data processing: 3 cores count the objects and maintain 3 counter dictionaries separately, 3 cores generate the 3 summary tables separately, and 1 core prints the output.

This method does not have a good performance, which runs 375.54s on 1 node 8 cores and 374.31s on 2 node 8 cores. Its running speed is similar to sequential execution and almost not accelerated by adding more nodes. This also suggests that once read from disk into memory, subsequent data processing is not a time-consuming procedure in this case.

### Conclusion
During the procedures of social media big data processing, reading data from disks is the most time-consuming procedure, and most requires parallel execution. For parallel reading, splitting the data file with each part read by one core is a recommended method, which has a significant speedup, at the expense of negligible decrease in accuracy. Parallel processing of data is not worth trying in this case, because once the data is read from disk into memory, subsequent operations are performed in memory, which cannot be significantly accelerated.
