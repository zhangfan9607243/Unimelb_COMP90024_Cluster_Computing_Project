# Unimelb Comp90024 Cluster Computing Project

## Acknowledgments
Thanks to the Unimelb COMP90024 2023S1 teaching team for providing this project opportunity and to the Unimelb SPARTAN HPC facility for providing computational resources.

## Project Introduction
This project implements a parallelized application for analyzing Twitter data, utilizing the University of Melbourne's High-Performance Computing (HPC) facility, SPARTAN. 

The main objectives of this assignment are, given a JSON file that contains Tweets and a `sal.json` dictionary that maps suburbs to their corresponding Greater Capital cities, to:
- Task 1: Count the number of different tweets made in the Greater Capital cities of Australia.
- Task 2: Identify the Twitter accounts that have made the most tweets.
- Task 3: Identify the users that have tweeted from the most different Greater Capital cities.

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

### 2. If You CANNOT Access Unimelb SPARTAN HPC (Run Locally)
#### (1) Data Preparation
First, you can access the data through the following ways.
  * `sal.json`: Already contained in the `/data/` of this repository.
  * `tinyTwitter.json`: Already contained in the `/data/` of this repository.
  * `smallTwitter.json`: Access through the link: .
  * `bigTwitter.json`: Access through the link: .

Then, you can put these data files in the `/data/` path of the cloned repository on your local device.
