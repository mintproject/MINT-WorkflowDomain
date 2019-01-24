import pickle
from datetime import datetime, timedelta
from netCDF4 import num2date, date2num
import sys

with open(sys.argv[1], 'rb') as handle:
    dict_out = pickle.load(handle)

dates = num2date(dict_out['time']['values'][:],dict_out['time']['units'])
dict_out['dates']={'values':dates, 'calendar':sys.argv[2], 'units':'NA'}

with open(sys.argv[3],"wb") as handle:
    pickle.dump(dict_out, handle, protocol=pickle.HIGHEST_PROTOCOL)
