#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Economic Model."""

import os
import csv
import sys
from pathlib import Path
import pandas as pd



def _main():
    year = sys.argv[2]
    region = sys.argv[3]
    o_land = Path("landdata.csv")
    o_yield = Path("yielddata.csv")
    o_price = Path("pricedata.csv")
    o_land = o_land.open("w",newline = '')
    o_land = csv.writer(o_land)
    o_land.writerow(("","calib"))
    o_yield = o_yield.open("w",newline = '')
    o_yield = csv.writer(o_yield)
    o_yield.writerow(("","calib"))
    o_price = o_price.open("w",newline = '')
    o_price = csv.writer(o_price)
    o_price.writerow(("","calib"))
    df = pd.read_csv(sys.argv[1], dtype=object)
    #print(df.head())
    #print(year)
    #print(region)
    values = df[(df['year']==year) & (df['region']==region)]
    #print(values.head())
    for index,row in values.iterrows():
        o_land.writerow((row['crop'],row['land_area']))
        o_yield.writerow((row['crop'],row['crop_yield']))
        o_price.writerow((row['crop'],row['crop_price']))
        #print(str(row['land_area']))
        #print(str(row['crop_yield']))
        #print(str(row['crop_price']))

if __name__ == "__main__":
	_main()

