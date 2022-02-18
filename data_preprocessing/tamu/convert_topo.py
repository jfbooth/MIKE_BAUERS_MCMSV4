import numpy as np 
import matplotlib.pyplot as plt
import scipy.io as sio
import xarray as xr
from netCDF4 import Dataset

import os, glob

#### Main code 
'''
Convert the topographic information into the format required by the tracker. 
'''

## Reading in ERA-Interim data
# checking the era interim invariants to see if they are the same size as this dataset
erai_file = '/localdrive/drive6/erai/converts/invariants.nc'
erai_ds = xr.open_dataset(erai_file)
erai_hgt = erai_ds.isel(time=0).hgt.values
erai_lsm = erai_ds.isel(time=0).lsm.values
erai_ds.close()

# sample SLP file to get the proper time
slp_file = '/localdrive/drive9/TAMU/SLP_REGRID/slp_tamu_1950.nc'
 
ds = xr.open_dataset(slp_file)
ds = ds.isel(time=0)
slp_lat = ds.lat.values
slp_lon = ds.lon.values
slp = ds.slp.values
start_time = ds.time.values
ds.close()

in_file = '/localdrive/drive9/TAMU/sample_hght_wrong_lat.nc'
out_file = '/localdrive/drive6/tamu/converts/invariants.nc'

orig_ds = xr.open_dataset(in_file)

# copying over the dataset values
ds = orig_ds.copy()

# getting the dataset values for the provided single time step
ds = ds.isel(time=0)
lat = ds.lat.values
lon = ds.lon.values
hgt = ds.hgt.values
ds.close()

# flipping the hgt and lat
out_lat = np.flipud(lat)

out_hgt = np.zeros((1, hgt.shape[0], hgt.shape[1]))
## either use the ERA-Interim height or the height from TAMU dataset
# out_hgt[0, :, :] = np.flipud(hgt)
out_hgt[0, :, :] = np.flipud(erai_hgt)

orig_ds['lat'] = out_lat
for key in ds.lat.attrs: 
    orig_ds['lat'].attrs[key] = ds.lat.attrs[key]
    
orig_ds['hgt'] = (['time', 'lat', 'lon'], out_hgt)
for key in ds.hgt.attrs: 
    orig_ds['hgt'].attrs[key] = ds.hgt.attrs[key]
    
    
out_lsm = np.zeros((1, hgt.shape[0], hgt.shape[1]))
out_lsm[0, :, :] = np.flipud(erai_lsm)
orig_ds['lsm'] = (['time', 'lat', 'lon'], out_lsm)
orig_ds['lsm'].attrs['standard_name'] = 'land_binary_mask'
orig_ds['lsm'].attrs['long_name'] = 'Land-sea Mask'
orig_ds['lsm'].attrs['units'] = '(0 - 1)'

orig_ds.to_netcdf(out_file)
print(f'Completed Creation of netcdf file!')

os.system(f'ncdump -h {out_file}')
