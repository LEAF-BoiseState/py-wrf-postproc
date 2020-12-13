#!/bin/bash

export year=$1
export vol=$2
export dom=$3
export yaml_file=$4 

export CreateDailySummary=1
export wrfout_path=/mnt/wrf_history/${vol}/wrf_out/wy_${year}/${dom}/
export wrfout_expr='wrfout_d0*'
export subset_path=/home/aflores/scratch/wrf_30yr_subsets_v2/${year}
export subset_expr=$5
export daily_path=/home/aflores/scratch/wrf_30yr_daily_summaries


mkdir ${subset_path}
mkdir ${daily_path}

python3 wrf-subsetter.py ${CreateDailySummary} ${wrfout_path} ${wrfout_expr} ${subset_path} ${subset_expr} ${daily_path} ${yaml_file}