import yaml
import sys
import xarray as xr
import time
import glob

def subset_vars(argv):

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

    yaml_varkeep_name = yaml_varkeep_path+yaml_varkeep_file

    # Get the name of the variables to be subset
    with open(yaml_varkeep_name,'r') as file_keep:
        var_keep_dict = yaml.full_load(file_keep)
    
    var_keep_list = [ sub['var_name'] for sub in var_keep_dict ]

    # Open the wrfout file using Xarray
    ds_wrf = xr.open_dataset(innc_name)

    # Get the subset by passing the list of variable names to keep to 
    # the *lazily opened* raw wrfout dataset 
    ds_wrf_subset = ds_wrf[var_keep_list]

    # Copy the attributes of the raw WRF dataset to the new subset dataset
    ds_wrf_subset.attrs = ds_wrf.attrs

    # Save the output dataset to the specified netcdf file name 
    ds_wrf_subset.to_netcdf(path=outnc_name)

return
