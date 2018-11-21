#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 14:12:29 2018

@author: deborahkhider

Transformation code from CYCLES output to Crop model
"""
#import numpy as np
import tarfile
import pandas as pd
import csv
import os
import numpy as np
import sys
#
#CYCLES needs to be run twice. One is the baseline scenario. The second has an
#increase in 10% fertilizer. 
#
percent_fertilizer = 0.1 #This should become a parameter

# select the year. In its present configuration only one year is allowed
year = 2017

# Set the tarfiles path
path = '/Users/deborahkhider/Documents/MINT/ECON/DataTransformation/12-month demo/'
# make sure to navigate to that path
os.chdir(path)
#%% Grab a list of the tar files
crop_names = []
for file in os.listdir(path):
    if file.endswith(".tar.gz") and file.startswith("Cycles"):
       crop_name = file.split('-')[1]
       if crop_name not in crop_names:
           crop_names.append(crop_name)
       
#%% Go over each crop and perform calculations.              
# prepare a dictionary
el_dict={}

for crop in crop_names:
    base_run_file = path +'Cycles-'+crop+'-baseline-results.tar.gz'
    scenario_run_file = path+'Cycles-'+crop+'-10_percent_inc-results.tar.gz'
    
    # Open the base tar file
    base_run = tarfile.open(name = base_run_file)
    base_run_names = base_run.getnames()
    for item in base_run_names:
        if 'season' in item:
            file_name = item
            base_file = base_run.extract(item)
    
    # Open the files and look for the grain yield
    data = pd.read_table(path+file_name, delimiter = '\t',\
                         skiprows = [1], index_col=False)
    
    # Make sure the dates are in datetime format
    for item in list(data):
        if 'DATE' in item:
            header_time = item
        if 'GRAIN YIELD' in item:
            header = item    
            
    data[header_time] = pd.to_datetime(data[header_time])
    time = data[header_time].dt.year.unique()
    base_grain= data.groupby(data[header_time].dt.year)[header].transform('mean').unique()
    
    # Do the same with the increased fertilizer run
    scenario_run = tarfile.open(name = scenario_run_file)
    scenario_run_names = scenario_run.getnames()
    for item in scenario_run_names:
        if 'season' in item:
            file_name = item
            scenario_file = scenario_run.extract(item)
    
    # Open the files and look for the grain yield
    data = pd.read_table(path+file_name, delimiter = '\t',\
                         skiprows = [1], index_col=False)
    
    # Get the Grain yield and data header
    for item in list(data):
        if 'DATE' in item:
            header_time = item
        if 'GRAIN YIELD' in item:
            header = item    
            
    data[header_time] = pd.to_datetime(data[header_time])
    scenario_grain= data.groupby(data[header_time].dt.year)[header].transform('mean').unique()
    
             
    # Calculate the yield %
    percent_yield = (scenario_grain-base_grain)/base_grain    
    #elasticity
    el_dict[crop] = percent_yield/percent_fertilizer

#%% Make sure the year is available
if year in time:
    index = np.where(time==year)[0][0]
else:
    sys.exit("Year not available in Cycles run")
        

#%% write out as csv file
csv_file = path+'cyclesdata2016.csv'

crops_econ = ['Cassava','Groundnuts','Maize','Sesame','Sorghum']
default_value = ['0.25','0.25','0.11','0.25','0.11']

with open(csv_file,'w',newline='') as csvfile:
    yieldwriter = csv.writer(csvfile, delimiter=',')
    yieldwriter.writerow(['','ybarN'])
    for idx, crop_econ in enumerate(crops_econ):
        if crop_econ in crop_names:
           yieldwriter.writerow([crop_econ,el_dict[crop_econ][index]]) 
        else:   
            yieldwriter.writerow([crop_econ,default_value[idx]])