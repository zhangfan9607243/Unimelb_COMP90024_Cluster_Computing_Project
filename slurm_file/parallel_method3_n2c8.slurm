#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --time=0-12:00:00

module load mpi4py/3.0.2-timed-pingpong
module load python/3.7.4
module load numpy/1.18.0-python-3.7.4

time mpiexec -n 8 python3 parallel_method3.py
my-job-stats -a -n -s