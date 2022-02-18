from netCDF4 import Dataset
import numpy as np
import glob
import os

# out_folder = '/localdrive/drive7/mdtf/slp_convert/fullaero/6hr'
# in_folder = '/localdrive/drive7/mdtf/slp/c96L32_am4g9_fullaero_MDTF_b6_2008To2012/atmos/ts/6hr/1yr'

out_folder = '/localdrive/drive7/mdtf/slp_convert/naud/6hr'
in_folder = '/localdrive/drive7/mdtf/slp/c96L48_am4b6_DDFull_Naud_partest1/atmos/ts/6hr/1yr'


model_year_range = [2008, 2012]
in_file_format = 'atmos.%d010100-%d123123.slp.nc'
out_file_format = 'slp.%04d.nc'


def get_hours_since_year(time):
  ''' Get time variable for a given year. Here time is given in days since, so we have to convert it to hours'''

  time_size = time.shape[0]
  time_delta = 24*(time[6]  - time[5])
  time = np.arange(0, (time_size)*time_delta, time_delta)

  return time

def create_slp_file(nc_file, out_file, year):

  # Reading in the data
  ncid = Dataset(nc_file,'r')
  lat = ncid.variables['lat'][:] # lat
  lon = ncid.variables['lon'][:] # lon

  ps = ncid.variables['slp'][:] # surface pressure, pascals
  time = ncid.variables['time'][:] # no_leap, time since 0001-01-01 00:00:00

  ncid.close()

  # slp = ps/100 # converting to mb 
  slp = ps # already in mb
  # time = get_hours_since_1850(2005, time) # converting time from hours since start of year, to hours since 1850

  time = get_hours_since_year(time)

  ncid = Dataset(out_file, 'w')

  ncid.createDimension('lon',lon.shape[0])
  ncid.createDimension('lat',lat.shape[0])
  ncid.createDimension('time',time.shape[0])

  nc_lon = ncid.createVariable('lon', np.float32, ('lon',))
  nc_lat = ncid.createVariable('lat', np.float32, ('lat',))
  nc_time = ncid.createVariable('time', np.float32, ('time',))
  nc_slp = ncid.createVariable('slp', np.float32, ('time','lat','lon'))

  nc_lat.units = 'degrees_north'
  nc_lon.units = 'degrees_east'
  nc_time.units = 'hours since %d-01-01 00:00:00'%(year)
  nc_slp.units = 'mb'

  nc_lat.axis = 'Y'
  nc_lon.axis = 'X'
  nc_time.calendar = 'proleptic_gregorian'
  nc_slp.long_name = 'Sea Level Pressure'

  nc_lat[:] = lat
  nc_lon[:] = lon
  nc_time[:] = time
  nc_slp[:] = slp

  ncid.close()

##############################################################
######################## MAIN ################################
##############################################################

for num in range(model_year_range[0], model_year_range[1]+1):
  # nc_file  = '/mnt/drive1/jj/MCMS/VEE/seasonal_aquaplanet.atmos_native.%04d010100-%04d123123.ps.nc'%(num, num)

  # netcdf input file
  nc_file = os.path.join(in_folder, in_file_format%(num, num))

  # output file  
  out_part_file = out_file_format%(num)
  out_file = os.path.join(out_folder, out_part_file)

  # calling the function that creates the SLP variable
  create_slp_file(nc_file, out_file, num)

  print ('Completed Year %d'%(num))

