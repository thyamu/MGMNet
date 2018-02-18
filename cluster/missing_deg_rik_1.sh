!/bin/sh
#SBATCH --job-name=deg_rik
#SBATCH --array=1-20
#SBATCH -t 0-12:00                  # wall time (D-HH:MM)
#SBATCH --qos=normal                # QOS "queue"
#SBATCH -o out/deg_rik_%A_%j.out             # STDOUT (%j = JobId)
#SBATCH -e error/deg_rik_%A_%j.err             # STDERR (%j = JobId)
#SBATCH --mail-type=FAIL       # notifications for job done & fail
#SBATCH --mail-user=hkim8@alumni.nd.edu # send-to ad

module load gcc/4.9.2
module load python/2.7.9
listVar=(6
10
11
13
3425
3426
3428
3433
3435
3437
3444
3447
3451
3452
3453
3459
3472
3483
3484
3490)
runID=${listVar[$(($SLURM_ARRAY_TASK_ID-1))]}
python ../code/deg_dist.py ranRxn ri k $runID
