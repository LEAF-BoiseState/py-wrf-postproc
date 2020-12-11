import numpy as np
import pandas as pd
import calendar as cd
import SubsetRCCZO_hourly_file
import sys

beg_yr = 2011 
end_yr = 2014
wy = np.linspace(beg_yr,end_yr,(end_yr - beg_yr + 1))

path_to_rcczo_hr = '/scratch/aflores/rcczo_temp/'
path_to_rcczo_day = '/scratch/aflores/rcczo_temp/daily_summaries/'

if(len(sys.argv)!=2):
    print('\nSubsetRCCZO_hourly_dataset\n')

case = sys.argv[1]

if(case == 'temp'):
    rcczo_hr_var_list = [('air_temperature/','ta_','surface_temperature','C')]
elif(case == 'snow'):
    rcczo_hr_var_list = [('percent_snow/','pcts_','pct_snow','decimal_percent')]
elif(case == 'relhum'):
    rcczo_hr_var_list = [('relative_humidity/','rh_','relative_humidity','decimal_percent')]
elif(case == 'dewpoint'):
    rcczo_hr_var_list = [('dew_point_temperature/','dp_','dew_point_temperature','C')]
elif(case == 'precip'):
    rcczo_hr_var_list = [('precipitation_depth/','precip_','precipitation_amount','mm')]
elif(case == 'solar'):
    rcczo_hr_var_list = [('solar_experimental/','cloud_solar_','net_solar','W/m^2')]
else:
    print('\nUnrecognized case... exiting\n')
    sys.exit(1)

for i in np.arange(len(rcczo_hr_var_list)):

    rcczo_var_path = rcczo_hr_var_list[i][0]
    rcczo_var_base = rcczo_hr_var_list[i][1]

    for j in np.arange(wy.size):
        
        # Check to see if water year is a leap year
        if(cd.isleap(int(wy[j]))):
            ndays = 366
        else:
            ndays = 365
        
        new_time = pd.date_range(str(int(wy[j]-1))+'-10-01', freq='H', periods=ndays*24)
        
        rcczo_hr_file = rcczo_var_base+'wy'+str(int(wy[j]))+'.nc'

        if(rcczo_hr_var_list[i][2]=='surface_temperature'):
            operator    = ['mean','min','max']
            out_var     = ['TMEAN','TMIN','TMAX']
            description = ['"Daily mean temperature"','"Daily minimum temperature"','"Daily maximum temperature"']

        elif(rcczo_hr_var_list[i][2]=='pct_snow'):
            operator    = ['mean']
            out_var     = ['pct_snow']
            description = ['"Daily mean percent snow cover"']

        elif(rcczo_hr_var_list[i][2]=='relative_humidity'):
            operator    = ['mean']
            out_var     = ['relative_humidity']
            description = ['"Daily mean relative humidity"']

        elif(rcczo_hr_var_list[i][2]=='dew_point_temperature'):
            operator    = ['mean']
            out_var     = ['dew_point_temperature']
            description = ['"Daily mean dew point temperature"']

        elif(rcczo_hr_var_list[i][2]=='precipitation_amount'):
            operator    = ['sum']
            out_var     = ['precipitation_amount']
            description = ['"Daily total precipitation"']
            
        elif(rcczo_hr_var_list[i][2]=='net_solar'):
            operator    = ['mean']
            out_var     = ['net_solar']
            description = ['"Daily average solar radiation"']


        for k in np.arange(len(operator)):
            rcczo_day_file = rcczo_var_base+operator[k]+'_wy'+str(int(wy[j]))+'_daily'+'.nc'
            SubsetRCCZO_hourly_file.HourlyToDaily(path_to_rcczo_hr+rcczo_var_path, rcczo_hr_file, \
                path_to_rcczo_day+rcczo_var_path, rcczo_day_file, rcczo_hr_var_list[i][2], \
                out_var[k], operator[k], description[k], rcczo_hr_var_list[i][3], new_time)


