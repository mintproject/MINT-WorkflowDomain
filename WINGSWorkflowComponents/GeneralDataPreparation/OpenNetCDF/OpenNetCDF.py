from netCDF4 import MFDataset
import pickle
import sys

def getKeys(nc_fid):
    '''Get the variables names in the NetCDF file'''
    keys=[]
    nc_vars = [var for var in nc_fid.variables]
    for vars in nc_vars:
        keys.append(getattr(nc_fid.variables[vars],'long_name'))
    return keys
        
def getMFNcVar(nc_fid, keys):
    ''' Extract variables from a dataset across multiple netCDF files.
    
    This function gets the variable contained in a netCDF file 
    and return them into Python nested dictionaries. The first
    dictionary's key contains the longname, while the
    second dictionary contains values, standard name (CF),
    units and the missing data flag.
    
    Args:
        nc_files (list): A list of netCDF files containing the dataset
        keys (list): A list of keys to fetch the variables according
            to the CF standard
    
    Returns:
        dict_out (dict): A dictionary containing the standard names as keys and
            the associated data as values.
    '''
    
    nc_vars = [var for var in nc_fid.variables]
    
    #Make empty lists to collect the info
    #longname (should be using the CF conventions)
    nc_vars_longname=[]
    #Units
    nc_vars_units=[]
    # Get the standard name
    nc_vars_standardname=[]
    #Corrections
    nc_vars_scale_factor=[]
    nc_vars_add_offset=[]
    #Missing values
    nc_vars_missing_value=[]
    
    for vars in nc_vars:
        if 'long_name' in nc_fid.variables[vars].ncattrs():
            nc_vars_longname.append(getattr(nc_fid.variables[vars],'long_name'))
        else:
            nc_vars_longname.append(vars)
        if 'units' in nc_fid.variables[vars].ncattrs():
            nc_vars_units.append(getattr(nc_fid.variables[vars],'units'))
        else:
            nc_vars_units.append('NA')
        if 'standard_name' in nc_fid.variables[vars].ncattrs():
            nc_vars_standardname.append(getattr(nc_fid.variables[vars],'standard_name'))
        else:
            nc_vars_standardname.append("NA")    
        if 'scale_factor' in nc_fid.variables[vars].ncattrs():
            nc_vars_scale_factor.append(getattr(nc_fid.variables[vars],'scale_factor'))
        else:
            nc_vars_scale_factor.append(1)
        if 'add_offset' in nc_fid.variables[vars].ncattrs():
            nc_vars_add_offset.append(getattr(nc_fid.variables[vars],'add_offset'))
        else:
            nc_vars_add_offset.append(0) 
        if 'missing_value' in nc_fid.variables[vars].ncattrs(): 
            nc_vars_missing_value.append(getattr(nc_fid.variables[vars],'missing_value'))
        else:
            nc_vars_missing_value.append('NA')
    # Check for the list against the desired variables and output.
    dict_out ={}
    for name in nc_vars_longname:
        if name in keys:
            f = {'values':[],'units':[],'missing_value':[], 'standard_name':{}}
            idx = nc_vars_longname.index(name)
            f['values']=(nc_fid.variables[nc_vars[idx]][:]*nc_vars_scale_factor[idx])\
                +nc_vars_add_offset[idx]
            f['units']=nc_vars_units[idx]
            f['missing_value'] = nc_vars_missing_value[idx]
            f['standard_name'] = nc_vars_standardname[idx]
            dict_out[name] = f
    
    return dict_out

files = [sys.argv[1],sys.argv[2],sys.argv[3]]

file_names =[]
for name in files:
    file_names.append(name)
    
#Open the file and get the keys for this example
nc_fid = MFDataset(file_names)
keys = getKeys(nc_fid)
dict_out=getMFNcVar(nc_fid,keys)

with open(sys.argv[4],"wb") as handle:
    pickle.dump(dict_out, handle, protocol=pickle.HIGHEST_PROTOCOL)