#!/bin/bash

export base_dir=$1
export search_str=$2
export outnc_base=$3

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


YearLen=${#YearArray[@]}

for (( i=0; i<${YearLen}; i++)); do

    year=${YearArray[$i]}

    search_dir=${base_dir}wy${year}/

    outnc_file=${outnc_base}${search_str}_wy${year}_daily_summary.nc

    echo python3 rollup_daily_summaries.py ${search_dir} ${search_str} ${outnc_file}

done


