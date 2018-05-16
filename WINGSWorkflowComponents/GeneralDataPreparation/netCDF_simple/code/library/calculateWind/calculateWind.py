import pickle
import numpy as np
import re
import sys

with open(sys.argv[1], 'rb') as handle:
    dict_out = pickle.load(handle)
    
U = np.array(dict_out['10 metre U wind component']['values'])
V = np.array(dict_out['10 metre V wind component']['values'])

W = np.sqrt(U**2+V**2)

dict_out['Wind Speed']={'values':W,'units':dict_out['10 metre V wind component']['units']}

#Get the wind height
s = '10 metre U wind component'
m = re.findall(r'\d+', s)[0]
dict_out['Wind reference height']={'values':int(m),'units':dict_out['10 metre V wind component']['units']}

with open(sys.argv[2],"wb") as handle:
   pickle.dump(dict_out, handle, protocol=pickle.HIGHEST_PROTOCOL)
