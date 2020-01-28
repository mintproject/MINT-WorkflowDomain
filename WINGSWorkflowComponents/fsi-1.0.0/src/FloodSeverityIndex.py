#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 13:57:38 2019

@author: deborahkhider

Calculate flood sevrity index based on volumetric flow threshold.
Returns one file for every  year.
"""
import matplotlib
matplotlib.use('Agg')

import xarray as xr
import numpy as np
import glob as glob
from datetime import date
import sys
import ast
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import os
import imageio
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

def openDataset(data, thresholds, year, bounding_box):
    ''' Open the thresholds and GloFAS concatenated dataset for the appropriate year

    Args:
        data (str): path to GloFAS in netcdf format. All years in one file
        thresholds (str): Name of the netcdf file containing the thresholds data
        year (list): year to consider
        bounding_box (list): min_lon, max_lon, min_lat, max_lat

    Returns:
        val (numpy array): Q values cut to the bounding box
        Q2 (numpy array): Threshold Q for a 2-yr flood
        Q5 (numpy array): Theshold Q for a 5-yr flood
        Q20 (numpy array): Threshold Q for a 20-yr flood
        lat (numpy array): latitude vector
        lon (numpy array): longitude vector
        time (numpy array): time vector
    '''
    data = xr.open_dataset(data)
    min_year = np.min(year)
    min_time = str(min_year)+'-01-01T00:00:00.000000000'
    max_year = np.max(year)
    max_time = str(max_year)+'-12-31T00:00:00.000000000'
    p_ = data.sel(lat=slice(bounding_box[3], bounding_box[2]),\
                  lon=slice(bounding_box[0],bounding_box[1]),
                  time = slice(min_time,max_time))
    val = p_.dis24.values
    #open thresholds
    thres = xr.open_dataset(thresholds)
    t_ = thres.sel(lat=slice(bounding_box[3], bounding_box[2]),\
                  lon=slice(bounding_box[0],bounding_box[1]))
    Q5 = t_['Q_5'].values
    Q2 = t_['Q_2'].values
    Q20 = t_['Q_20'].values

    lat = p_['lat'].values
    lon = p_['lon'].values
    time = p_['time'].values

    return val, Q2, Q5, Q20, lat, lon, time
    

def openDatasets(data,thresholds,year,bounding_box):
    '''Open the thresholds and GloFAS datasets for the appropriate year

    Args:
        data (str): path to GloFAS in netcdf format. Data needs to be oragnized in yearly folders
        thresholds (str): Name of the netcdf file containing the thresholds data
        year (list): year to consider
        bounding_box (list): min_lon, max_lon, min_lat, max_lat

    Returns:
        val (numpy array): Q values cut to the bounding box
        Q2 (numpy array): Threshold Q for a 2-yr flood
        Q5 (numpy array): Theshold Q for a 5-yr flood
        Q20 (numpy array): Threshold Q for a 20-yr flood
        lat (numpy array): latitude vector
        lon (numpy array): longitude vector
        time (numpy array): time vector
    '''
    # path + folders
    path = data+'/'+str(year)
    nc_files = (glob.glob(path+'/*.nc'))
    file_names=[]
    for file in nc_files:
        file_names.append(file)
    file_names.sort()
    #open
    data = xr.open_mfdataset(file_names)
    p_ = data.sel(lat=slice(bounding_box[3], bounding_box[2]),\
                  lon=slice(bounding_box[0],bounding_box[1]))
    val = p_.dis24.values

    #open thresholds
    thres = xr.open_dataset(thresholds)
    t_ = thres.sel(lat=slice(bounding_box[3], bounding_box[2]),\
                  lon=slice(bounding_box[0],bounding_box[1]))
    Q5 = t_['Q_5'].values
    Q2 = t_['Q_2'].values
    Q20 = t_['Q_20'].values

    lat = p_['lat'].values
    lon = p_['lon'].values
    time = p_['time'].values

    return val, Q2, Q5, Q20, lat, lon, time

def calculateIndex(val, Q2, Q5, Q20, lat, lon, time):
    '''Calculate a flooding index based on threshold levels

    The flooding index is boolean. 1: medium flood (2-yr retrun period ),
    2: high (5-yr retrun period) and 3: severe (20-yr return period)

    Args:
       val (numpy array): Q values cut to the bounding box
       Q2 (numpy array): Threshold Q for a 2-yr flood
       Q5 (numpy array): Theshold Q for a 5-yr flood
       Q20 (numpy array): Threshold Q for a 20-yr flood
       lat (numpy array): latitude vector
       lon (numpy array): longitude vector
       time (numpy array): time vector

    Returns:
        flood_bool (numpy array): the boolean index for flood severity

    '''
# put a boolean for flood level, 0: no flood, 1: Q2, 2: Q5, 3: Q20
    flood_bool = np.zeros(np.shape(val))

    for idx_time, i_time in enumerate(time):
        for idx_lat, i_lat in enumerate(lat):
            for idx_lon, i_lon in enumerate(lon):
                if val[idx_time,idx_lat,idx_lon]>=Q20[idx_lat,idx_lon]:
                    flood_bool[idx_time,idx_lat,idx_lon]= 3
                elif val[idx_time,idx_lat,idx_lon]<Q2[idx_lat,idx_lon]:
                    flood_bool[idx_time,idx_lat,idx_lon] = 0
                elif val[idx_time,idx_lat,idx_lon]>=Q2[idx_lat,idx_lon] and val[idx_time,idx_lat,idx_lon]<Q5[idx_lat,idx_lon]:
                    flood_bool[idx_time,idx_lat,idx_lon] = 1
                elif val[idx_time,idx_lat,idx_lon]>=Q5[idx_lat,idx_lon] and val[idx_time,idx_lat,idx_lon]<Q20[idx_lat,idx_lon]:
                    flood_bool[idx_time,idx_lat,idx_lon] = 2
                elif np.isnan(val[idx_time,idx_lat,idx_lon]):
                    flood_bool[idx_time,idx_lat,idx_lon] = np.nan

    return flood_bool

def writeNetcdf(flood_bool, lat, lon, time, year):
    ''' Write netcdf with the flooding index

    Args:
        flood_bool (numpy array): Boolean arrays containing the flood severity index
        lat (numpy array): Vector of latitudes
        lon (numpy array): Vector of longtidues
        time (numpy array): Vector of time
        year (int): year of interest
    '''
    #write as a data array
    da_flood = xr.DataArray(flood_bool,coords=[time,lat,lon],dims=['time','lat','lon'])
    da_flood.attrs['title'] = 'Flood level Severity (medium, high, and severe)'
    da_flood.attrs['long_name'] = 'Flood Level Severity'
    da_flood.attrs['units'] = 'unitless'
    da_flood.attrs['valid_min'] = 0
    da_flood.attrs['valid_max'] = 3
    da_flood.attrs['missing_value'] = np.nan
    da_flood.attrs['standard_name'] = 'channel_water_flow__flood_volume-flux_severity_index'

    ds = da_flood.to_dataset(name='flood')
    ds.attrs['title'] = "Flood Severity"
    ds.attrs['summary'] = 'Flood severity index: medium (2-yr flood, index=1),'+\
        'high (5-yr flood, index=2), and severe (20-yr flood, index=3), inferred from'+\
        'the GloFAS dataset. Thresholds were determined by fitting a Gumbel extreme'+\
        ' value distribution to the yearly maxima in each grid cell over 1981-2017.'
    ds.attrs['date_created'] = str(date.today())
    ds.attrs['creator_name'] = 'Deborah Khider'
    ds.attrs['creator_email'] = 'khider@usc.edu'
    ds.attrs['institution'] = 'USC Information Sciences Institute'
    ds.attrs['geospatial_lat_min'] = np.min(lat)
    ds.attrs['geospatial_lat_max'] = np.max(lat)
    ds.attrs['geospatial_lon_min'] = np.min(lon)
    ds.attrs['geospatial_lon_max'] = np.max(lon)
    ds.attrs['time_coverage_start'] = str(ds.time.values[0])
    ds.attrs['time_coverage_end'] = str(ds.time.values[-1])
    ds.attrs['time_coverage_resolution'] = 'daily'
    
    if os.path.isdir('./results') is False:
        os.makedirs('./results')

    ds.to_netcdf('./results/GloFAS_FloodIndex_'+str(year)+'.nc')

def visualizeFlood(allflood, lat, lon, alltime):
    proj = ccrs.PlateCarree()
    idx = np.size(alltime)
    count = list(np.arange(0,idx,1))
    filenames =[]

    #Make a directory for results/figures if it doesn't exit
    if os.path.isdir('./figures') is False:
        os.makedirs('./figures')
    if os.path.isdir('./results') is False:
        os.makedirs('./results')
    
    for i in count:
        v = allflood[i,:,:]
        date = pd.to_datetime(alltime[i]).strftime("%d %B %Y")  
        fig,ax = plt.subplots(figsize=[15,10])
        ax = plt.axes(projection=proj)
        ax.add_feature(cfeature.BORDERS)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.RIVERS)
        img = plt.contourf(lon, lat, v, [0,1,2,3,4],
            colors = ['white','orange','#FF4500','#B22222'],               
            transform=proj)
        cbar = plt.colorbar(img, orientation='horizontal',pad=0.1)
        cbar.ax.set_title('Flood Severity Index')
        cbar.ax.set_xticklabels(['None','Medium','High','Severe',''])
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                      linewidth=2, color='gray', alpha=0.5, linestyle='--')
        gl.xlabels_top = False
        gl.ylabels_right = False
        gl.xlines = False
        gl.ylines = False
        gl.xlocator = mticker.FixedLocator(np.linspace(np.round(np.min(lon)),np.round(np.max(lon)),5))
        gl.ylocator = mticker.FixedLocator(np.linspace(np.round(np.min(lat)),np.round(np.max(lat)),5))
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 12, 'color': 'gray'}
        gl.ylabel_style = {'size': 12, 'color': 'gray'}
        #Add a title with time
        plt.title(date, fontsize=18, loc='left', pad=1)
        #save a jepg
        filename = './figures/flooding_t'+str(date)+'.jpeg'
        filenames.append(filename)
        plt.savefig(filename)
        plt.close(fig)
    
    #create a gif
    writer = imageio.get_writer('./results/Flooding_index.mp4', fps=5)
    for filename in filenames:
        writer.append_data(imageio.imread(filename))
    writer.close()
    
if __name__ == "__main__":
    #params
    bounding_box = ast.literal_eval(sys.argv[3])
    year = ast.literal_eval(sys.argv[4])
    thresholds = sys.argv[2]
    data = sys.argv[1]
    fig = ast.literal_eval(sys.argv[5])

    #Run the functions in a row
    if data.endswith('.nc')==True:
        val, Q2, Q5, Q20, lat, lon, time = openDataset(data,thresholds,year,bounding_box)
        flood_bool = calculateIndex(val, Q2, Q5, Q20, lat, lon, time)
        writeNetcdf(flood_bool, lat, lon, time, 'all')
        if fig == True:
            visualizeFlood(flood_bool, lat, lon, time)

    else:    
        for y in year:
            val, Q2, Q5, Q20, lat, lon, time = openDatasets(data,thresholds,y,bounding_box)
            flood_bool = calculateIndex(val, Q2, Q5, Q20, lat, lon, time)
            writeNetcdf(flood_bool, lat, lon, time, y)
            if fig  == True:
                try: allflood = np.concatenate((allflood,flood_bool),axis=0)
                except NameError: allflood = flood_bool
                try: alltime = np.concatenate((alltime,time),axis=0)
                except NameError: alltime = time
    
            if fig == True:
                visualizeFlood(allflood, lat, lon, alltime)
