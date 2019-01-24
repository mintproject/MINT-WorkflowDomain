#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 13:34:01 2018

@author: deborahkhider

This routine uses FLDAS climatology to
generate possible weather conditions
for an area given a percent level with
respect to observed conditions. The
routine prepares the CSV file for use with
the weather generator. 
"""

import sys
import xarray as xr
import numpy as np
import os
import glob
import pandas as pd
import csv

def startup(path_monthly, path_daily, flagP, min_lon, max_lon,\
               min_lat, max_lat,min_month,max_month,level):
    '''Calls the righ method for dataset_source

    Args:
        path_monthly (str): The path to the directory containing the netCDF files
            for the monthly data
        path_daily (str): The path to the directory containing the netCDF files
            for the daily data
        flagP (str): Name of the variable of interest as declared in the file
        min_lon (float): Minimum longitude for the bounding box
        max_lon (float): Maximum longitude for the bounding box
        min_lat (float): Minimum latitude for the bounding box
        max_lat (float): Maximum latitude for the bounding box
        min_month (int): The first month of the season of interest
        max_month (int): The last month of the season of interest
        level (float): The level at which to do the analysis

    '''

    # First make a few assertions to make sure that everything works
    assert min_lon<max_lon, "Maximum longitude smaller than minimum longitude"
    assert min_lat<max_lat, "Maximum latitude smaller than minimum latitude"
    assert min_month<max_month, "Maximum month smaller than minimum month"

    # Return the mean climatology
    dt_mean = clim_FLDAS(path_monthly, flagP, min_lon, max_lon,\
               min_lat, max_lat,min_month,max_month)

    # Find the year use as basis for comparison
    year = findYear(dt_mean, level)
    FLDAS_to_csv(year, min_month, max_month, min_lat, max_lat,\
               min_lon, max_lon)

def clim_FLDAS(path_monthly, flagP, min_lon, max_lon,\
               min_lat, max_lat,min_month,max_month):
    '''Calculate climatology for the FLDAS data

    This function takes the seasonal average over several years
    to estimate the climatology and deviation for a specipic year.
    Works only for FLDAS monthly datasets.

    Args:
        path (str): The path to the directory containing the netCDF files
        flagP (str): Name of the variable of interest as declared in the file
        min_lon (float): Minimum longitude for the bounding box
        max_lon (float): Maximum longitude for the bounding box
        min_lat (float): Minimum latitude for the bounding box
        max_lat (float): Maximum latitude for the bounding box
        min_month (int): The first month of the season of interest
        max_month (int): The last month of the season of interest
        year (int): The year of interest for the comparison

    Returns:
        'climatology.csv': The average for all years
        dt_mean (pandas dataframe): The monthly weather
    '''

    # Get the name of all the netCDF file in the directory
    # Assumes that the files are organized as per the FLDAS
    # datasets.
    subdirs = [os.path.join(path_monthly, o) for o in os.listdir(path_monthly)
                        if os.path.isdir(os.path.join(path_monthly,o))]

    nc_files= []

    for d in subdirs:
        files = glob.glob(d+'/*.nc')
        for file in files:
            nc_files.append(file)

    if not nc_files:
        sys.exit('No available datasets')

    # Go through the files and make calculations
    years = []
    months = []
    P = []
    season = np.arange(min_month,max_month+1,1)
    for file in nc_files:
        nc_fid = xr.open_dataset(file)
        time = nc_fid.coords['time'].values[0]
        month = time.astype('datetime64[M]').astype(int) % 12 + 1
        if month in season:
            lon = nc_fid.coords['X'].values
            lat = nc_fid.coords['Y'].values
            # Make sure that there is something to bound
            assert min_lat<np.max(lat), "Minimum latitude out of range"
            assert max_lat>np.min(lat), "Maximum latitude out of range"
            assert min_lon<np.max(lon), "Minimum longitude out of range"
            assert max_lon>np.min(lon), "Maximum longitude out of range"

            # Get the bounding box indices
            idx_x = np.arange(np.where(lon>min_lon)[0][0],\
                              np.where(lon<max_lon)[0][-1],1)

            idx_y = np.arange(np.where(lat>min_lat)[0][0],\
                              np.where(lat<max_lat)[0][-1],1)

            # Make sure the variable is in the file
            assert flagP in nc_fid, 'Variable not in dataset.'
            # Grab the appropriate data
            data_temp = nc_fid[flagP].values[:,idx_y,:]
            data = data_temp[:,:,idx_x]
            #Remove missing values
            flag_miss = nc_fid.attrs['missing_value']
            # Replace by NaN
            data = data.astype('float')
            data[data==flag_miss]=np.nan
            # Take the average
            P.append(np.nanmean(data))
            # Get the time
            years.append(time.astype('datetime64[Y]').astype(int) + 1970)
            months.append(time.astype('datetime64[M]').astype(int) % 12 + 1)
            nc_fid.close()
        else:
            nc_fid.close()

    # Place the data into a dataframe
    dt = pd.DataFrame({'Years':years,'Months':months,'Data':P})
    # Take the average for each year
    dt_mean = pd.DataFrame({'Years':dt['Years'].unique(),
            'Data': dt.groupby(['Years'])['Data'].transform('mean').unique()})

    # Write as csv file
    #cwd = os.getcwd()
    #dt_mean.to_csv(cwd+'/climatology.csv', sep =',')

    return dt_mean

# Find the year to model
def findYear(dt_mean, level):
    '''Find an comparison year

    Using the climatology, find a year with the same appropriate
    climate to generate weather from

    Args:
        - dt_mean (pandas dataframe): Dataframe containing averages for the
        months of interest.
        - level: The level for comparison (e.g. 60% of historical rainfall)

    Returns:
        - year (int): The year, available in the daily datasets, that would
            be the most appropriate for comparison.

    '''

    # Find the index corresponding to a 60% level
    prob = int(round(level * dt_mean['Data'].count()))
    # Order the dataframe
    dt_sort = dt_mean.sort_values(['Data'])
    year = np.array(dt_sort['Years'])[prob-1]
    index_up = 0
    while year not in np.arange(2001,2017,1):
        index_up+= 1
        year = np.array(dt_sort['Years'])[prob-1+index_up]
    year = np.array(dt_sort['Years'])[prob-1]
    index_down=0
    while year not in np.arange(2001,2017,1):
        index_down-=1
        year = np.array(dt_sort['Years'])[prob-1+index_down]

    #Choose the closest neighbor
    if abs(index_down)<index_up:
        year = np.array(dt_sort['Years'])[prob-1+index_down]
    else:
        year = np.array(dt_sort['Years'])[prob-1+index_up]

    return year

def FLDAS_to_csv(year, min_month, max_month, min_lat, max_lat,\
               min_lon, max_lon):
    ''' Prepare file for WGENW

    This method prepares the  csvfile to run the weather generator

    Args:
        - year (int): The year of interest. Ontained from findYear method
        - min_month (int): The first month of the season of interest
        - max_month (int): The last month of the season of interest
        - min_lat (float): The minimum latitude for the bounding box
        - max_lat (float): The maximum latitude for the bounding box
        - min_lon (float): The minimum longitude for the bounding box
        - max_lon (float): The maximum longitude for the bounding box

    '''
    #Get the season
    season = np.arange(min_month,max_month+1,1)
    # Get a csv file ready
    csv_file = str(os.getcwd())+'/FLDAS_WGEN.csv'
    #Start a counting index for the station ID.
    id_idx = 1
    #Density of water
    rho_w = 997
    with open(csv_file,'w',newline='') as csvfile:
        wgenwriter = csv.writer(csvfile, delimiter=',')
        wgenwriter.writerow(['station id','lon','lat',\
                             'year','month','min. temperature',
                             'max. temperature','cloud fraction',
                             'wind speed','precipitation','wet'])
        for month in season:
            if month<10:
                month_str='0'+str(month)
            else:
                month_str=str(month)
            subdir = path_daily+'/'+str(year)+'/'+month_str
            nc_files = (glob.glob(subdir+'/*.nc'))
            # open the data
            nc_fid = xr.open_mfdataset(nc_files)
            # Get the index for lat/lon
            lats = np.where(np.logical_and(nc_fid['Y'].values>=min_lat, nc_fid['Y'].values<=max_lat))[0]
            lons = np.where(np.logical_and(nc_fid['X'].values>=min_lon, nc_fid['X'].values<=max_lon))[0]
            # Get the missing value flag
            flag_miss = nc_fid.attrs['missing_value']
            for lat_idx in lats:
                for lon_idx in lons:
                    #Next generate a station_id
                    if len(str(id_idx))==1:
                        station_ID = 'FLDAS_0000'+str(id_idx)
                    elif len(str(id_idx))==2:
                        station_ID = 'FLDAS_000'+str(id_idx)
                    elif len(str(id_idx))==3:
                        station_ID = 'FLDAS_00'+str(id_idx)
                    elif len(str(id_idx))==4:
                        station_ID = 'FLDAS_0'+str(id_idx)
                    elif len(str(id_idx))==5:
                        station_ID = 'FLDAS_'+str(id_idx)
                    else:
                        sys.exit('Station_ID index out of bounds')
                    ## Deal with temperature
                    # Replace missing values
                    data = nc_fid['Tair_f_tavg'].values
                    data = data.astype('float')
                    data[data==flag_miss]=np.nan
                    #Calculate minT and maxT
                    minT = np.nanmin(data[:,lat_idx,lon_idx])- 273.15 #Convert to C
                    maxT = np.nanmax(data[:,lat_idx,lon_idx])- 273.15 #Convert to C
                    ## wind speed
                    # Replace missing values
                    data = nc_fid['Wind_f_tavg'].values
                    data = data.astype('float')
                    data[data==flag_miss]=np.nan
                    # Take the average for the month
                    avWind =np.nanmean(data[:,lat_idx,lon_idx])
                    # Precipitation
                    data = nc_fid['Rainf_f_tavg'].values
                    data = data.astype('float')
                    data[data==flag_miss]=np.nan
                    # Calculate the total for the month
                    totP = np.nansum(data[:,lat_idx,lon_idx])
                    # Convert to mm/day
                    totP = totP*1000*86400/rho_w
                    # Number of wet days in a month
                    wet_days = len(np.where(data[:,lat_idx,lon_idx]>0)[0])
                    # Write it out
                    wgenwriter.writerow([station_ID,str(round(nc_fid['X'].values[lon_idx],2)),\
                                         str(round(nc_fid['Y'].values[lat_idx],2)),\
                                         str(year), str(month),str(round(minT,2)),\
                                         str(round(maxT,2)),'0.5',str(round(avWind,2)),\
                                         str(round(totP,2)),str(wet_days)])
                    # Close netcdf file
                    nc_fid.close()
                    # update the counter
                    id_idx+=1
#%% Execute
path_monthly = sys.argv[1]
path_daily = sys.argv[2]
flagP = sys.argv[3]
min_lon = float(sys.argv[4])
max_lon = float(sys.argv[5])
min_lat = float(sys.argv[6])
max_lat = float(sys.argv[7])
min_month = int(sys.argv[8])
max_month = int(sys.argv[9])
level = float(sys.argv[10])

startup(path_monthly, path_daily, flagP, min_lon, max_lon,\
               min_lat, max_lat,min_month,max_month,level)