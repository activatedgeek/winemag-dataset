#!/usr/bin/env bash

#SBATCH --job-name={{ name }}
#SBATCH --output={{ dir }}/stdout.log
#SBATCH --error={{ dir }}/stderr.log
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=sanyam@nyu.edu
#SBATCH --nodes=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=24:00:00

# Activate Environment
source ~/.bash_profile
conda activate winemag

export DATASET_DIR=${DATA_DIR}/winemag-dataset

mkdir -p ${DATASET_DIR}

pushd ${SRC_DIR}/winemag-dataset

scrapy crawl winemag -s JOBDIR={{ dir }}/state \
                     -a start_page={{ start_page }} -a end_page={{ end_page }} \
                     -o ${DATASET_DIR}/winemag-{{ start_page }}-{{ end_page }}.csv

popd
