## Subsetting Example with Xarray - using a large 30-year climate dataset
### Charlie Becker
### 04-30-19

This generates a subset of 30 files, one for each water year with a time dimention of 365/366 which is aggregated from hourly data.  Modification for different domains, temporal schemes, and variables should be fairly intuitive. 

The varlist file contains a full list of variables for the currrent dataset we're pulling from.  Such lists can be generated through list(< nc_file >.variables

It is neccessary to comment OUT the variables you want to INCLUDE in your subset, as this is a brief work around that allows a subset of specific variables within the multi-file function open_mfdataset().  The 'data_vars = [list of str] should be able to specify targeted variables, but for unknown reasons this dataset pulls all variables even under the data_vars = 'minimal' constriant. We thus feed 'drop_variables = ' our custum variable list as an alternative. The variable 'XTIME' must remain commented out for any temporal adjustments, as it is the coordinate variable depended upon for transformation.

As a base size estimation, a seven single layered variable subset averaged by day, equates to ~ 35 GB over 30 years.  

