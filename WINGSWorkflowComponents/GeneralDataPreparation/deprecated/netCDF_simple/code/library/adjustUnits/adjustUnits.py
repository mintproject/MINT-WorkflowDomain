import pickle
import sys

with open(sys.argv[1], 'rb') as handle:
    dict_out = pickle.load(handle)
    
f2 = open(sys.argv[2],'r') 
var = f2.readlines()
var = [x.strip() for x in var]

f3 =  open(sys.argv[3],'r')
units = f3.readlines()
units = [x.strip() for x in units]

for idx, item in enumerate(var):
    dataUnits = dict_out[item]['units']
    if dataUnits != units[idx]:
        #print("Adjusting "+item+' units...')
        P = dict_out['Surface pressure']['values']/100
        dict_out['Surface pressure']={'values':P,'units':'mbar','notes':'units have been converted'}
        
with open(sys.argv[4],"wb") as handle:
    pickle.dump(dict_out, handle, protocol=pickle.HIGHEST_PROTOCOL)
