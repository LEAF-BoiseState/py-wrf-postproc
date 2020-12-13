import sys      # Required for capturing command line args 
import glob     # Required for getting wrfout file names (and paths)
import yaml     # Required for parsing input yaml file

import WRFPostProcFuncs # Local file that contains post-processing functions

def main(argv):

    # Check for correct number of inputs and throw error and usage statement
    if(len(argv)!=7):
        print('\nusage: wrf-subsetter.py <CreateDailySummary> <wrfout path> <wrfout file expr.> <subset path>')
        print('\t\t <subset file expr.> <daily summary path> <yaml config file>\n')
        print('\t <CreateDailySummary>: 0 (Fals) or 1 (True). Also create daily summary.')
        print('\t <wrfout path>:        Path to wrfout file directory (all wrfouts will be subset)')
        print('\t <wrfout file expr.>:  Expression to specifically identify wrfout files')
        print('\t <subset path>:        Path to subset ')
        print('\t <subset file expr.>:  String to denote subset - replaces "wrfout" in file name')
        print('\t <daily summary path>: Path to outut for daily summary files')
        print('\t <yaml config. file>:  Name of yaml config file (incl. path)')
        print('\t All parameters required... pass empty strings for unused parameters')
        sys.exit(1)

    # Set default values of variables
    SubsetVars=True
    CreateDailySummary=True

    # Determine if daily summary creation was turned off by used 
    if(int(argv[0])==0):
        CreateDailySummary=False

    # Parse argv to get the parameters to run the scripts
    wrfout_path     = argv[1] #'/Users/lejoflores/data/wrfout_test/'
    wrfout_file_exp = argv[2] #'wrfout_d02*'
    subset_path     = argv[3] # '/Users/lejoflores/py-wrf-postproc/'
    subset_file_exp = argv[4] # 'landmodel'
    daily_path      = argv[5] # '/Users/lejoflores/py-wrf-postproc/'
    daily_file_exp  = '_daily_summary'
    yaml_var_file   = argv[6] # 'config2.yml'

    # Construct the correct search expression for wrfout files and get the file names as a list
    wrfout_search_exp = wrfout_path+wrfout_file_exp
    wrfoutfiles = glob.glob(wrfout_search_exp)

    # Open the yaml file that contains the variables to be subset and information about
    # how they will be transformed into daily summary data
    with open(yaml_var_file,'r') as yaml_file:
        wrf_var_dict = yaml.full_load(yaml_file)

    # Create a list of only variable names to be subset. This is passed to xarray to actually
    # subset the variables from the (lazily loaded) full wrfout dataset
    wrf_var_list = [ sub['var_name'] for sub in wrf_var_dict ]

    # Loop over the wrfout files
    for wrfoutnc in wrfoutfiles:

        if(SubsetVars):

            # The following set of string operations create a correct output 
            # file name:

            # Strip the full file name of the wrfout path
            subsetnc = wrfoutnc.replace(wrfout_path,'')

            # Replace 'wrfout' in the file name with the subset file 
            # identifier expression
            subsetnc = subsetnc.replace('wrfout',subset_file_exp)
         
            # Replace the '_00:00:00' with '.nc'
            subsetnc = subsetnc.replace('_00:00:00','.nc')

            # Append the output subset path
            subsetnc = subset_path+subsetnc
            
            WRFPostProcFuncs.subset_vars('', wrfoutnc, '', subsetnc, wrf_var_list)

        if(CreateDailySummary):

            if(SubsetVars):

                # The following set of string operations take the previously created
                # subset netCDF file name and further transform it into a correct file name
                # (incl. path) in which to write the daily summary
                ncin_name = subsetnc

                outnc_name = subsetnc.replace(subset_path,daily_path)
                outnc_name = outnc_name.replace('.nc',daily_file_exp+'.nc')
            else:
                # For now, this isn't used but, in principle, a user might want to create 
                # daily summaries from the raw wrfouts

                # Dealing with the wrfout
                ncin_name = wrfoutnc

                # Strip the full file name of the wrfout path
                outnc_name = wrfoutnc.replace(wrfout_path,'')

                # Replace 'wrfout' in the file name with the subset file 
                # identifier expression
                outnc_name = outnc_name.replace('wrfout',subset_file_exp)
             
                # Replace the '_00:00:00' with '.nc'
                outnc_name = outnc_name.replace('_00:00:00',daily_file_exp+'.nc')

                # Append the output subset path
                outnc_name = daily_path+outnc_name

            WRFPostProcFuncs.create_daily_dataset('', ncin_name, '', outnc_name, wrf_var_dict)

if __name__ == '__main__':
    main(sys.argv[1:])

