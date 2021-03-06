import numpy as np
import xarray as xr
import zarr

subset_key = 'forcing'
base_dir = '/home/aflores/scratch/wrf_30yr_subsets/forcing/'


def nc_to_zarr(wy_ss_dir, zarr_store):

    ds = xr.open_mfdataset(wy_ss_dir+'/*.nc', concat_dim='Time', combine='nested')

    ds.to_zarr(zarr_store, consolidated=True)

    print('Completed output to '+zarr_store)

    return

for year in np.arange(1988,2018):

    wy_ss_dir = base_dir+'wy'+'{:d}'.format(year)

    zarr_store = wy_ss_dir+'-'+subset_key+'.zarr'

    #print('wy_ss_dir = '+wy_ss_dir)
    #print('zarr_store = '+zarr_store)

    nc_to_zarr(wy_ss_dir, zarr_store)


