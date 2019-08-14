#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 14:16:53 2018

@author: deborahkhider

This routine takes the output of the weather
generator and put it back into FLDAS-like data.
"""
import xarray as xr
import numpy as np
import os
import pandas as pd
import sys

def csv_to_FLDAS(wgen_out, wgen_in, path_out, file_prefix):
    '''Transform the output WGEN csv file into NetCDF files
    
    This method transforms the output csv file from the weather generator
    WGEN into a netCDF file following FLDAS format. The netCDF files are
    output to path_out following the same file structure. All subfolders
    are created automatically.
    
    Args:
        wgen_out: The csv file output from the weather generator
        wgen_in: The csv file input to the weather generator
        path_out: an existing directory in which to write out the netCDF files
        file_prefix: A prefix for the netcdf files
    
    '''
    
    # Get the csv files into pandas dataframe
    data_out = pd.read_table(wgen_out, delimiter = ',',index_col=False)
    data_in = pd.read_table(wgen_in, delimiter = ',',index_col=False)
        
    #Density of water
    rho_w = 997
    
    # Get the lat/lon bounds
    min_lat = np.min(data_in['lat'])
    max_lat = np.max(data_in['lat'])
    min_lon = np.min(data_in['lon'])
    max_lon = np.max(data_in['lon'])
    
    # Make the coordinates
    step = 0.1
    lats = np.arange(min_lat,max_lat,step)
    # carefully handle the end
    if abs(max_lat-lats[-1])>0.000001:
        lats = np.append(lats,max_lat)
    lons = np.arange(min_lon,max_lon,step)
    # carefully handle the end
    if abs(max_lon-lons[-1])>0.000001:
        lons = np.append(lons,max_lon)
    
    # Add latitude/longitude to data_out
    data_out['lat'] =np.nan
    data_out['lon'] =np.nan
    for idx, row in data_out.iterrows():
        station_id = (row['id'])
        data_out.at[idx,'lat'] = data_in.loc[data_in['station id'] == station_id]['lat']
        data_out.at[idx,'lon'] = data_in.loc[data_in['station id'] == station_id]['lon']
    # Get the time bounds
    timestamp = pd.to_datetime(data_out[['year','month','day']])
    # Add to dataframe
    data_out['timestamp']=timestamp
    # Calculate mean T
    data_out['meanT'] =np.nan
    for idx, row in data_out.iterrows():
        data_out.at[idx,'meanT'] = np.mean([data_out['tmin'][idx],data_out['tmax'][idx]])
    # Find the unique values in timestamp
    timestamp_unique = timestamp.unique()
    for ts in timestamp_unique:
        data_out_time = data_out.loc[data_out['timestamp'] == ts]
        # Tranform to panda datetime to make xarray happy. 
        ts = pd.to_datetime([ts])
        # Get the variables and reshape
        T = np.array(data_out_time['meanT']).reshape((1,lats.shape[0],lons.shape[0]))+273.15 #convert to K
        W = np.array(data_out_time['wind']).reshape((1,lats.shape[0],lons.shape[0]))
        P = np.array(data_out_time['prcp']).reshape((1,lats.shape[0],lons.shape[0]))*rho_w/(1000*86400)
        # Start putting everything in xarray dataarrays
        temp = xr.DataArray(T,
                            coords = [('time',ts),('Y',lats),('X',lons)],
                            attrs = {'standard_name':'air_temperature',
                                     'long_name':'air temperature',
                                     'units':'K',
                                     'vmin':np.min(T),
                                     'vmax':np.max(T),
                                     'cell_methods':'time:mean'})
        
        precip = xr.DataArray(P,
                            coords = [('time',ts),('Y',lats),('X',lons)],
                            attrs = {'standard_name':'rainfall_flux',
                                     'long_name':'rainfall flux',
                                     'units':'kg m-2 s-1',
                                     'vmin':np.min(P),
                                     'vmax':np.max(P),
                                     'cell_methods':'time:mean'})
            
        wind = xr.DataArray(W,
                            coords = [('time',ts),('Y',lats),('X',lons)],
                            attrs = {'standard_name':'wind_speed',
                                     'long_name':'wind speed',
                                     'units':'m s-1',
                                     'vmin':np.min(W),
                                     'vmax':np.max(W),
                                     'cell_methods':'time:mean'})
        
        X_attr = {'standard_name':'longitude',
                  'long_name':'longitude',
                  'axis':'X',
                  'units':'degrees_east'}
    
        Y_attr = {'standard_name':'latitude',
                  'long_name':'latitude',
                  'axis':'Y',
                  'units':'degrees_north'}
        
        # Create the dataset
        nc_fid = xr.Dataset(data_vars = {'Tair_f_tavg': temp,
                                         'Wind_f_tavg':wind,
                                         'Rainf_f_tavg':precip},
                            attrs = {'Conventions':'CF-1.4',
                                     'missing_value':-9999.0,
                                     'title': 'WGEN output',
                                     'comment': 'Outputs generated from WGEN'}) 
        
        nc_fid.X.attrs.update(X_attr)
        nc_fid.Y.attrs.update(Y_attr)
        
        # save the file  
        # Create the year directory if needed
        new_dir = path_out+'/'+str(ts.year[0])
        try:
            os.stat(new_dir)
        except:
            os.mkdir(new_dir)
        # Create a new_subdirecotry if needed 
        if len(str(ts.month[0]))==1:
            str_month = '0'+str(ts.month[0])
        else:
            str_month = str(ts.month[0])
        new_subdir = new_dir +'/'+str_month
        try:
            os.stat(new_subdir)
        except:
            os.mkdir(new_subdir)    
        # Write out the files
        if len(str(ts.day[0]))==1:
            str_day = '0'+str(ts.day[0])
        else:
            str_day = str(ts.day[0])    
        filename = file_prefix+str(ts.year[0])+str_month+str_day+'.001.nc'
        path = new_subdir+'/'+filename
        nc_fid.to_netcdf(path)
        
#%% Execute  
wgen_out = sys.argv[1] #wgen_out = '/Users/deborahkhider/Documents/GitHub/simplewg/WGEN_out.csv'
wgen_in = sys.argv[2] #wgen_in = '/Users/deborahkhider/Documents/GitHub/simplewg/FLDAS_WGEN.csv'
path_out = sys.argv[3] #path_out = '/Users/deborahkhider/Documents/MINT/Climate/Scenarios/FLDAS_WGEN'
file_prefix = sys.argv[4] #file_prefix = 'FLDAS_NOAH01_A_EA_D.A' 

csv_to_FLDAS(wgen_out, wgen_in, path_out, file_prefix)       