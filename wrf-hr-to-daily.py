
import yaml
import sys
import xarray as xr
import numpy as np

import WRFPostProcFuncs


def main(argv):

    # Error trap number of command line arguments
    if(len(argv) != 5):
        print("\nusage: wrf-hr-to-daily.py <yaml file> <in nc file path> <in nc file name>")
        print("             <out nc file path> <out nc file name>\n")
        print("\t<yaml file>: ")
        print("\t<in nc file path>: ")
        print("\t<in nc file name>: ")
        print("\t<out nc file path>: ")
        print("\t<out nc file name>: ")
        sys.exit()

    # Parse command line arguments
    yaml_name = argv[0] # Name of yaml file (including path if not in the same folder)

    ncin_path = argv[1] # Path to the input netcdf file of hourly data
    ncin_name = argv[2] # Name of the netcdf file of hourly data

    ncout_path = argv[3] # Path to where output daily data will be stored
    ncout_name = argv[4] # Name of output daily summary netcdf file

    # Open the yaml config file and load it into a dictionary
    with open(yaml_name,'r') as file:
        var_keep_dict = yaml.full_load(file)

    # Call the create_daily_dataset function in WRFPostProcFuncs
    WRFPostProcFuncs.create_daily_dataset(ncin_path, ncin_name, ncout_path, ncout_name, var_keep_dict)

    # Complete... return control
    return

if __name__ == '__main__':
    main(sys.argv[1:])
