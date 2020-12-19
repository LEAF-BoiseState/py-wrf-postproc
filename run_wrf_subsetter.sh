#!/bin/bash

#export year=$1
#export vol=$2
export dom=$1
export yaml_file=$2
export subset_expr=$3

declare -a YearArray=('1987'
                      '1988'
                      '1989'
                      '1990'
                      '1991'
                      '1992'
                      '1993'
                      '1994' 
                      '1995' 
                      '1996' 
                      '1997' 
                      '1998'
                      '1999'
                      '2000'
                      '2001'
                      '2002'
                      '2003'
                      '2004'
                      '2005'
                      '2006'
                      '2007'
                      '2008'
                      '2009'
                      '2010'
                      '2011'
                      '2012'
                      '2013'
                      '2014'
                      '2015'
                      '2016'
                      '2017'
                      )

declare -a VolArray=('vol01'
                     'vol02'
                     'vol02'
                     'vol02'
                     'vol02'
                     'vol02'
                     'vol02'
                     'vol03'
                     'vol03'
                     'vol03'
                     'vol03'
                     'vol03'
                     'vol03'
                     'vol04'
                     'vol04'
                     'vol05'
                     'vol05'
                     'vol06'
                     'vol06'
                     'vol07'
                     'vol07'
                     'vol08'
                     'vol08'
                     'vol09'
                     'vol09'
                     'vol10'
                     'vol10'
                     'vol11'
                     'vol11'
                     'vol12'
                     'vol12'
                     )


YearLen=${#YearArray[@]}

for (( i=0; i<${YearLen}; i++)); do

    year=${YearArray[$i]}
    vol=${VolArray[$i]}

    CreateDailySummary=1
    wrfout_path=/network-shares/wrf_history/${vol}/wrf_out/wy_${year}/${dom}/
    wrfout_expr='wrfout_d0*'
    subset_path=/network-shares/salmon/wrf_subsets/wrf_hourly/${subset_expr}/wy${year}/
    daily_path=/network-shares/salmon/wrf_subsets/wrf_daily/${subset_expr}/wy${year}/

    mkdir -p $subset_path
    mkdir -p $daily_path

    python3 wrf-subsetter.py ${CreateDailySummary} ${wrfout_path} ${wrfout_expr} ${subset_path} ${subset_expr} ${daily_path} ${yaml_file}

done
