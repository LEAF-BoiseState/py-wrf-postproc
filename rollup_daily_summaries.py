import xarray as xr
import glob
import sys


def main(argv):

    if(len(argv)!=3):
        print('usage: rollup_daily_summaries.py <search dir> <search str> <out nc file>\n')
        print('\t<search_dir>  = Directory in which netcdf files exist')
        print('\t<search_str>  = String to search for netcdf files in a single dataset')
        print('\t<out nc file> = Name of output file to export dataset to (with path)\n')
        sys.exit(1)

    search_dir = argv[0]
    search_str = argv[1]
    outncname = argv[2]

    ds = xr.open_mfdataset(search_dir+search_str+'*')

    ds.to_netcdf(outncname)

    return


if __name__ == '__main__':
    main(sys.argv[1:])
