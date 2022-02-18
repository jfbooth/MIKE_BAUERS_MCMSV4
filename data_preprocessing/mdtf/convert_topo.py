from netCDF4 import Dataset
import numpy as np
import glob
import os

# out_file = '/localdrive/drive7/mdtf/slp_convert/fullaero/6hr/mdtf_hgt.nc'
# in_file = '/localdrive/drive7/mdtf/c96L32_am4g9_fullaero_MDTF_b6_2008To2012/atmos/atmos.static.nc'
# var_name = 'oro'

out_file = '/localdrive/drive7/mdtf/slp_convert/naud/6hr/mdtf_hgt.nc'
in_file = '/localdrive/drive7/mdtf/slp/c96L48_am4b6_DDFull_Naud_partest1/atmos/atmos.static.nc'
var_name = 'zsurf'

def create_topo_file(nc_file, out_file):

  # Reading in the data
  ncid = Dataset(nc_file,'r')
  lat = ncid.variables['lat'][:] # lat
  lon = ncid.variables['lon'][:] # lon

  oro = ncid.variables[var_name][:] # surface pressure, pascals

  ncid.close()

  # slp = ps/100 # converting to mb 
  hgt = oro # already in mb
  # time = get_hours_since_1850(2005, time) # converting time from hours since start of year, to hours since 1850


  ncid = Dataset(out_file, 'w')

  ncid.createDimension('lon',lon.shape[0])
  ncid.createDimension('lat',lat.shape[0])

  nc_lon = ncid.createVariable('lon', np.float32, ('lon',))
  nc_lat = ncid.createVariable('lat', np.float32, ('lat',))
  nc_hgt = ncid.createVariable('hgt', np.float32, ('lat','lon'))

  nc_lat.units = 'degrees_north'
  nc_lon.units = 'degrees_east'
  nc_hgt.units = 'METERS'

  nc_lat.axis = 'Y'
  nc_lon.axis = 'X'
  nc_hgt.long_name = 'TOPOGRAPHY'

  nc_lat[:] = lat
  nc_lon[:] = lon
  nc_hgt[:] = hgt

  ncid.close()

##############################################################
######################## MAIN ################################
##############################################################


create_topo_file(in_file, out_file)

