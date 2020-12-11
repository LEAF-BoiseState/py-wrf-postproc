
import yaml
import sys
import xarray as xr
import numpy as np
import pandas as pd



def HourlyToDaily(input_path, input_file, in_var_name, out_var_name, operator, description, units):

    assert (operator=='sum' or operator=='mean' or operator=='max' or operator=='min'), \
        "Input operator must be sum, mean, min, or max" 

    # Open dataset, error check
    ds_wrf = xr.open_dataset(input_path+input_file, autoclose=True)

    assert ds_wrf, "Could not open dataset with "+input_path+input_file

    # TODO: Resample time? 
    #ds_rcczo['time'] = new_time

    if (operator=='sum'):
        da_wrf = ds_wrf[in_var_name].sum(dim='Time')
    elif (operator=='mean'):
        da_wrf = ds_wrf[in_var_name].mean(dim='Time')
    elif (operator=='min'):
        da_wrf = ds_wrf[in_var_name].min(dim='Time')
    elif (operator=='max'):
        da_wrf = ds_wrf[in_var_name].max(dim='Time')

    ds_wrf_new = da_wrf.to_dataset(name=out_var_name)
    ds_wrf_new[out_var_name].attrs = [('description', description),('units',units)]


    return ds_wrf_new

####

def main(argv):

    if(len(argv) != 7):
        print("\nFATAL ERROR: Not enough arguments\n")
        print("USAGE: wrf-hr-to-daily.py <yaml file path> <yaml file name> <in nc file path>")
        print("       <in nc file name> <out nc file path> <out nc file name>\n")
        print("\t<yaml file path>")
        print("\t<yaml file name>")
        print("\t<in nc file path>")
        print("\t<in nc file name>")
        print("\t<out nc file path>")
        print("\t<out nc file name>")
        sys.exit()

    yaml_path = argv[1]
    yaml_name = argv[2]

    ncin_path = argv[3]
    ncin_name = argv[4]

    ncout_path = argv[5]
    ncout_name = argv[6]

    with open(yaml_path+yaml_name,'r') as file:
        myinp = yaml.full_load(file)

    nvars = len(myinp)

    for i in np.arange(nvars):

        wrf_var_name = myinp[i].get('var_name')
        wrf_out_name = myinp[i].get('out_name')
        wrf_operator = myinp[i].get('operator')
        wrf_description = myinp[i].get('description')
        wrf_units = myinp[i].get('units')

        print('Variable '+str(i+1)+' is '+ wrf_var_name)
        print('\tOutput name is '+wrf_out_name)
        print('\tOperator is '+wrf_operator)
        print('\tDescription is '+wrf_description)
        print('\tUnits are '+wrf_units)

        ds_out = HourlyToDaily(ncin_path, ncin_name, wrf_var_name, wrf_out_name, wrf_operator, wrf_description, wrf_units)

        if(i>0):
            ds_dayout = xr.merge([ds_dayout, ds_out])
        else:
            ds_dayout = ds_out

    ds_dayout.to_netcdf(path=ncout_path+ncout_name)



if __name__ == '__main__':
    main(sys.argv)
