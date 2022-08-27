#/bin/bash
#BSUB -J NAME
#BSUB -e %J.err
#BSUB -o %J.out
#BSUB -n 1
#BSUB -q gauss
#BSUB -gpu "num=1:mode=exclusive_process"
python test_gpu.py