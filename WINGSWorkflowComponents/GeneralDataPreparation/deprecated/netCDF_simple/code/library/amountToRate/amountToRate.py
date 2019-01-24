import pickle
import numpy as np
import sys

with open(sys.argv[1], 'rb') as handle:
    dict_out = pickle.load(handle)
    
precip_rate = 1000*np.array(dict_out['Total precipitation']['values'])/3

dict_out['Precipitation rate'] = {'values':precip_rate.tolist(), \
                                  'units':'mm/hr','notes':\
                                  'converted from amount, Total precipitation'}

with open(sys.argv[2],"wb") as handle:
    pickle.dump(dict_out, handle, protocol=pickle.HIGHEST_PROTOCOL)
