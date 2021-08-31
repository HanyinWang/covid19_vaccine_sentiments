#!/bin/bash

# set date
date="2021-02-14"

# unload any modules that carried over from your command line session
module purge all

# load modules you need to use
module load python/anaconda3.6

# activate virtual environment 
conda config --prepend envs_dirs /home/hwi3319/anaconda3/envs
source activate twitter_vaccine_env

# merge all info
cd ./code/
python3 merge.py "${date}"  

# split vaccine-related tweets according to real date
# (remove all previous files before running)
cd ./code/
python3 split_to_daily.py

# get daily topic (sentiments: all, positive, or negative)
cd ./code/
python3 daily_topic.py "${date}" all