# Python-based Post-processing Tools for WRF Data
## Lejo Flores
## December 14, 2020

This repository provides several python-based, xArray-enabled scripts to facilitate the ability to easily subset raw `wrfout` output from the Weather Research and Forecasting (WRF) model and create daily summaries based on user-provided information. The user creates a YAML file that specifies which variable in the WRF output are to be subsetted, if and how they are to be reported at daily time-scales (i.e., daily sum, mean, max, min). Several example YAML files are provided for commonly required combinations of variables. 

Dependencies:
- xarray
- sys
- glob
- yaml
- numpy
