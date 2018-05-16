import pickle
import sys

with open(sys.argv[1], 'rb') as handle:
    dict_out = pickle.load(handle)
    
f2 = open(sys.argv[2],'r') 
var = f2.readlines()
var = [x.strip() for x in var]

for item in var:
    if item not in dict_out.keys():
        sys.exit('variables are missing')

with open(sys.argv[3],"wb") as handle:
    pickle.dump(dict_out, handle, protocol=pickle.HIGHEST_PROTOCOL)        
