#!/bin/bash
#SBATCH -J SubsetRCCZO_h2d         # Job name
#SBATCH -o SubsetRCCZO_h2d.o%j     # Output and error file name (%j expands to jobID)
#SBATCH -n 1                       # Total number of mpi tasks requested
#SBATCH -N 1                       # Total number of nodes at 16 mpi tasks per-node requested
#SBATCH -p leaf                    # Queue (partition) -- normal, development, etc.
#SBATCH -t 12:00:00                # Run time (hh:mm:ss) - 2.0 hours

python3 /home/aflores/scratch/rcczo_temp/SubsetRCCZO_hourly_dataset.py solar 

exit

 
