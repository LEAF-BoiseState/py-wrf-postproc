import yaml
import sys
import xarray as xr
import time
import glob

wrf_varlist_file = './wrf-varlist.yml'


def main(argv):

    if(len(argv)!=7):
        print("USAGE: wrf-subset-vars.py <in nc path> <in nc file> <out nc path> <out nc file> <var list path> <var list file>\n")
        sys.exit(1)


    innc_path = argv[1]
    innc_file = argv[2]

    innc_name = innc_path+innc_file

    outnc_path = argv[3]
    outnc_file = argv[4]

    outnc_name = outnc_path+outnc_file

    yaml_varkeep_path = argv[5]
    yaml_varkeep_file = argv[6]

    yaml_varkeep_name = yaml_varkeep_path+yaml_varkeep_name

    yaml_varall_name = wrf_varlist_file

    with open(yaml_varall_name,'r') as file_all:
        var_all = yaml.full_load(file_all)


    with open(yaml_varkeep_name,'r') as file_keep:
        var_keep = yaml.full_load(file_keep)

    wrf_drop = list(filter(var_keep['var_list'].__ne__, var_all['var_list']))


    ds_wrf_subset = xr.open_dataset(innc_name, drop_variables=wrf_drop)


    ds_wrf_subset.to_netcdf(path=outnc_name)

    return

if __name__ == '__main__':
    main(sys.argv)
