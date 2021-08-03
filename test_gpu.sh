#! /bin/bash
#$ -cwd
#$ -l inf
#$ -l vf=32G
#$ -l gpus=1
#$ -now y
#$ -m abes

bash ./create_venv.sh 

source env/bin/activate

python main.py