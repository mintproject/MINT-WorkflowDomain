import pickle
import numpy as np
import sys

with open(sys.argv[1], 'rb') as handle:
    dict_out = pickle.load(handle)
    
TD = np.array(dict_out['2 metre dewpoint temperature']['values'])
T = np.array(dict_out['2 metre temperature']['values'])
RH = 100*(np.exp((17.625*TD)/(243.04+TD))/np.exp((17.625*T)/(243.04+T)))

dict_out['Relative Humidity']={'values':RH,'units':'NA'} 

with open(sys.argv[2],"wb") as handle:
    pickle.dump(dict_out, handle, protocol=pickle.HIGHEST_PROTOCOL)
