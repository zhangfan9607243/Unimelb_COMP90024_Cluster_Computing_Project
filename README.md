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
