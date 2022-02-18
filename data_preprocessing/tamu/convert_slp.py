import numpy as np 
import matplotlib.pyplot as plt
import scipy.io as sio
import xarray as xr
from netCDF4 import Dataset

import os, glob

########
# looks like I don't need to convert the slp to make it work with the tracker 
# Jimmy already took care of this

#### Main code 
in_folder = '/localdrive/drive9/TAMU/SLP_REGRID'
out_folder = '/localdrive/drive6/tamu/converts/'
year_list = [1950, 2050]

print('Copying...')
for year in range(year_list[0], year_list[1]+1):

  # creating the filename
  in_fn = os.path.join(in_folder, f'slp_tamu_{year}.nc')
  out_fn = os.path.join(out_folder, f'slp.{year}.nc')

  cmd = f'cp {in_fn} {out_fn}'
  os.system(cmd)
  print(f'\t {year}')

  # # reading in the dataset
  # nc = Dataset(fn)
  # print(nc.variables.keys())
  # lat = nc['lat'][:]
  # lon = nc['lon'][:]
  # slp = nc['slp'][:]
  # print(slp.shape)
  # nc.close()
  #
  # plt.figure()
  # plt.pcolormesh(lon, lat, slp[0, :, :])
  # plt.colorbar()
  # plt.show()
  #
  # # break to test for a single year 
  # break
