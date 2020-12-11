import xarray as xr # Needed for subsetting
import numpy as np  # Needed for array operations
import sys          # Needed for system flow of control

# On R2: This is the location to the precip data:
# /mnt/reynoldsczo/precipitation_depth/

def HourlyToDaily(*argv):

	if(len(argv) != 10):
		print(" FATAL ERROR: Not enough arguments\n")
		print("USAGE: HourlyToDaily(PATH_TO_NC_FILE, NC_FILE_NAME, OUTPUT_PATH, OUTPUT_FILE,")
		print("\t\t IN_VAR_NAME, OUT_VAR_NAME, OPERATOR, DESCRIPTION, UNITS>\n")
		print("PATH_TO_NC_FILE = Absolute path of NetCDF file to be subsetted")
		print("NC_FILE_NAME    = Name of the netCDF file to be subsetted (with extension)")
		print("OUTPUT_PATH     = Absolute path of output file")
		print("OUTPUT_FILE     = Name of the output netCDF file")
		print("IN_VAR_NAME     = Name of variable in the input netCDF file")
		print("OUT_VAR_NAME    = Name of variable in the output netCDF file")
		print("OPERATOR        = sum, mean, min, or max")
		print("DESCRIPTION     = Text description of variable for metadata")
		print("UNITS           = Units of the output variable for metadata")
		print("NEW_TIME        = A new datetime64 object to address discrepencies in underlying dataset\n\n")
		sys.exit()

	input_path   = argv[0]
	input_file   = argv[1]
	output_path  = argv[2]
	output_file  = argv[3]
	in_var_name  = argv[4]
	out_var_name = argv[5]
	operator     = argv[6]
	description  = argv[7]
	units        = argv[8]
	new_time     = argv[9]

	assert (operator=='sum' or operator=='mean' or operator=='max' or operator=='min'), \
		"Input operator must be sum, mean, min, or max" 

	# Open dataset, error check
	ds_rcczo = xr.open_dataset(input_path+input_file)

	assert ds_rcczo, "Could not open file "+input_path+input_file

	ds_rcczo['time'] = new_time

	if (operator=='sum'):
		new_array = ds_rcczo[in_var_name].resample(time='24H').sum(dim='time')
	elif (operator=='mean'):
		new_array = ds_rcczo[in_var_name].resample(time='24H').mean(dim='time')
	elif (operator=='min'):
		new_array = ds_rcczo[in_var_name].resample(time='24H').min(dim='time')
	elif (operator=='max'):
		new_array = ds_rcczo[in_var_name].resample(time='24H').max(dim='time')

	new_dataset = new_array.to_dataset().rename({in_var_name : out_var_name}) # rename in_var_name to out_var_name

	new_dataset[out_var_name].attrs = [('description', description),('units',units)]
	new_dataset['y'] = ds_rcczo['y']
	new_dataset['x'] = ds_rcczo['x']

	print("Saving "+output_path+output_file+" now...")

	new_dataset.to_netcdf(path=output_path+output_file)

	print("Finished saving")

	return;