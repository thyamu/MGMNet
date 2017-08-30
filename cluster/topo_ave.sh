#!/bin/sh
#SBATCH -n 1                        # number of cores
#SBATCH -t 5-2:00                   # wall time (D-HH:MM)
#SBATCH -o log/slurm.%j.out             # STDOUT (%j = JobId)
#SBATCH -e log/slurm.%j.err             # STDERR (%j = JobId)
#SBATCH --mail-type=END,FAIL        # notifications for job done & fail
#SBATCH --mail-user=hyunju.kim@asu.edu # send-to address

module load gcc/4.9.2
module load python/2.7.9
python ../code/topo_ave_bio.py s k 1
