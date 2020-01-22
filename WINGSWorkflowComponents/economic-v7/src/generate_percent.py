#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Economic Model."""

import os
import csv
import sys
from pathlib import Path



def _main():
    
    crops = ["barley","maize","millet","pulses","sorghum","teff","wheat"]
    o_price = Path("simpricedata.csv")
    o_fert = Path("simfertsubsidy.csv")
    o_fert_con = Path("simfertcon.csv")
    w_price = o_price.open("w",newline = '')
    w_price = csv.writer(w_price)
    w_price.writerow(("","sim"))
    w_fert = o_fert.open("w",newline = '')
    w_fert = csv.writer(w_fert)
    w_fert.writerow(("","sim"))
    w_fert_con = o_fert_con.open("w",newline = '')
    w_fert_con = csv.writer(w_fert_con)
    w_fert_con.writerow(("","sim"))
    # price (1-7)
    # fertilizer subsidy (8-14)
    for i,crop in enumerate(crops):
        w_price.writerow((crop,sys.argv[i+1]))
        w_fert.writerow((crop,sys.argv[i+8]))
	
    # fertcon (15)
    sorghum_p = w_fert_con.writerow(("all",sys.argv[15])) 

if __name__ == "__main__":
	_main()

