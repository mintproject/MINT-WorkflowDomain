import pickle
import sys

f2 = open(sys.argv[2],'r') 
var = f2.readlines()
var = [x.strip() for x in var]

with open(sys.argv[1], 'rb') as handle:
    dict_out = pickle.load(handle)

warningsVar = []
for item in var:
    if item not in dict_out.keys():
       warningsVar.append(item)

f3 = open(sys.argv[4],'w')
for item in warningsVar:
   f3.write("%s\n" % item)            
f3.close()

with open(sys.argv[3],"wb") as handle:
    pickle.dump(dict_out, handle, protocol=pickle.HIGHEST_PROTOCOL)
