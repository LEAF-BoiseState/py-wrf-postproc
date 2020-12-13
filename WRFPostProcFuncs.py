import xarray as xr
import numpy as np
import glob
import warnings

warnings.filterwarnings("ignore", category=FutureWarning) 


def hourly_to_daily(input_path, input_file, in_var_name, out_var_name, operator, description, units, rain_bucket_vol):
    
    assert (operator=='sum' or operator=='mean' or operator=='max' or operator=='min'), \
        "Input operator must be sum, mean, min, or max" 

    # Open dataset, error check
    ds_wrf = xr.open_dataset(input_path+input_file)

    assert ds_wrf, "Could not open dataset with "+input_path+input_file

    ds_wrf = ds_wrf.swap_dims({'Time': 'XTIME'})

    # Special case: if one of the precipitation variables is RAINNC or RAINC, then
    # I_RAINNC or I_RAINC, respectively, needs to be added in before the resampling
    # makes any sense
    if((in_var_name=='RAINNC') or (in_var_name=='RAINC')):
        da_rain  = ds_wrf[in_var_name]
        da_irain = ds_wrf['I_'+in_var_name]

        temp1 = rain_bucket_vol*da_irain + da_rain
        temp2 = temp1.isel(XTIME=0) - rain_bucket_vol*da_irain.isel(XTIME=0)
        temp3 = temp1.diff('XTIME')

        da_rain_acc = xr.concat([temp2, temp3], 'XTIME')

        in_var_name = in_var_name+'_ACC'

        ds_wrf[in_var_name] = da_rain_acc

    if (operator=='sum'):
        da_wrf = ds_wrf[in_var_name].resample(XTIME='1D').sum(dim='XTIME')
    elif (operator=='mean'):
        da_wrf = ds_wrf[in_var_name].resample(XTIME='1D').mean(dim='XTIME')
    elif (operator=='min'):
        da_wrf = ds_wrf[in_var_name].resample(XTIME='1D').min(dim='XTIME')
    elif (operator=='max'):
        da_wrf = ds_wrf[in_var_name].resample(XTIME='1D').max(dim='XTIME')

    ds_wrf_new = da_wrf.to_dataset(name=out_var_name)

    if(in_var_name!='XTIME'):
        ds_wrf_new[out_var_name].attrs = [('description', description),('units',units)]

    return ds_wrf_new

def subset_vars(innc_path, innc_file, outnc_path, outnc_file, var_keep_list):

    # Create the name of the input file
    innc_name = innc_path+innc_file

    # Open the wrfout file using Xarray
    ds_wrf = xr.open_dataset(innc_name)

    # Get the subset by passing the list of variable names to keep to 
    # the *lazily opened* raw wrfout dataset 
    ds_wrf_subset = ds_wrf[var_keep_list]

    # Copy the attributes of the raw WRF dataset to the new subset dataset
    ds_wrf_subset.attrs = ds_wrf.attrs

    # Save the output dataset to the specified netcdf file name 
    ds_wrf_subset.to_netcdf(path=outnc_path+outnc_file)

    return

def create_daily_dataset(ncin_path, ncin_name, outnc_path, outnc_name, var_keep_dict):

    nvars = len(var_keep_dict)
    rain_bucket_vol = 100.0 # Default rain bucket size for RAINNC and RAINC

    for i in np.arange(nvars):

        wrf_var_name = var_keep_dict[i].get('var_name')
        wrf_out_name = var_keep_dict[i].get('out_name')
        wrf_operator = var_keep_dict[i].get('operator')
        wrf_description = var_keep_dict[i].get('description')
        wrf_units = var_keep_dict[i].get('units')

        if(wrf_var_name=='RAINNC') or (wrf_var_name=='RAINC'):
            if var_keep_dict[i].get('bucket_vol') is not None:
                rain_bucket_vol = var_keep_dict[i].get('bucket_vol')

        if(wrf_operator=='skip'):
            continue

        ds_out = hourly_to_daily(ncin_path, ncin_name, wrf_var_name, wrf_out_name, wrf_operator, wrf_description, wrf_units, rain_bucket_vol)

        if(i>0):
            ds_dayout = xr.merge([ds_dayout, ds_out])
        else:
            ds_dayout = ds_out

    ds_dayout.to_netcdf(path=outnc_path+outnc_name)

    return

