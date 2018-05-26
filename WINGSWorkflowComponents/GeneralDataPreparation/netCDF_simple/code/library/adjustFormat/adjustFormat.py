import pickle
import numpy as np
import sys

with open(sys.argv[1], 'rb') as handle:
    dict_out = pickle.load(handle)

f2 = open(sys.argv[2],'r') 
var = f2.readlines()
var = [x.strip() for x in var]

index = list(range(3,3+len(var)))

for idx, item in enumerate(var):
    dataValues = dict_out[item]['values']
    dataValues = np.float32(dataValues)
    f = open(sys.argv[index[idx]],'wb')
    #dataValues.byteswap(True)
    dataValues.tofile(f)
    f.close()
