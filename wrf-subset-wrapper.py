import glob


wrfout_path = '/Users/lejoflores/data/wrfout_test/'
wrfout_file_exp = 'wrfout_d02*'

subset_path = '/Users/lejoflores/Xarray_subset/'
subset_file_exp = 'forcings'

wrfout_search_exp = wrfout_path+wrfout_file_exp

wrfoutfiles = glob.glob(wrfout_search_exp)


for wrfoutnc in wrfoutfiles:

    subsetnc = wrfoutnc.replace(wrfout_path,'')
    print(subsetnc)

    subsetnc = subsetnc.replace('wrfout',subset_file_exp)
    print(subsetnc)

    subsetnc = subsetnc.replace('_00:00:00','.nc')
    print(subsetnc)

    subsetnc = subset_path+subsetnc
    print(subsetnc)

