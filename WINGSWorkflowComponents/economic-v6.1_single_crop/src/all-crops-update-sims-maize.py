#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Economic Model."""

import os
import csv
import sys
from pathlib import Path


def _generate_sim_price(p, sim_price):
	i = Path(p)
	o = Path("price_v6.1_onecrop.csv")

	with i.open("r") as r, o.open("w",newline = '') as w:
		r = csv.reader(r)
		w = csv.writer(w)
		
		num = 0
		for c, p in r:
			if c == "":
				w.writerow((c, p))
			else:
				p = float(p)
				w.writerow((c, round(p + (p * sim_price[num]), 2)))
				num += 1
			
			
	return o


def _generate_sim_production_cost(pc, sim_production_c1, sim_production_c2):
	i = Path(pc)
	o = Path("productioncost_v6.1_onecrop.csv")

	with i.open("r") as r, o.open("w",newline = '') as w:
		r = csv.reader(r)
		w = csv.writer(w)

		num = 0
		for c, c1, c2 in r:
			if c == "":
				w.writerow((c, c1, c2))
			else:
				c1 = float(c1)
				c2 = float(c2)
				w.writerow(
					(
						c,
						round(c1 + (c1 * sim_production_c1[num]), 2),
						round(c2 + (c2 * sim_production_c2[num]), 2),
					)
				)
				num += 1

	return o


def _main():
    
	base_p = sys.argv[1]
	base_c = sys.argv[2]

	#crops
	#cassava_p = float(sys.argv[3]) / 100
	#cassava_c1 = float(sys.argv[4]) / 100
	#cassava_c2 = float(sys.argv[5]) / 100
	
	#groundnuts_p = float(sys.argv[6]) / 100
	#groundnuts_c1 = float(sys.argv[7]) / 100
	#groundnuts_c2 = float(sys.argv[8]) / 100
	
	maize_p = float(sys.argv[3]) / 100
	maize_c1 = float(sys.argv[4]) / 100
	maize_c2 = float(sys.argv[5]) / 100
	
	#sesame_p = float(sys.argv[12]) / 100
	#sesame_c1 = float(sys.argv[13]) / 100
	#sesame_c2 = float(sys.argv[14]) / 100
	
	#sorghum_p = float(sys.argv[15]) / 100
	#sorghum_c1 = float(sys.argv[16]) / 100
	#sorghum_c2 = float(sys.argv[17]) / 100

	a_p = [maize_p]
	a_c1 = [maize_c1]
	a_c2 = [maize_c2]
	
	print(a_p[0])
	
	_generate_sim_price(base_p, a_p)
	_generate_sim_production_cost(base_c, a_c1, a_c2)


if __name__ == "__main__":
	_main()

