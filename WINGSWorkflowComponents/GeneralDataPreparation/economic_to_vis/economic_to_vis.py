#!/usr/bin/env python3

import configparser
import csv
import sys
import tempfile
from shutil import copyfile

config_file = sys.argv[1]
economic_files = sys.argv[2:-1]
output_file = sys.argv[-1:][0]

# configuration parameters
config = configparser.ConfigParser()
config.read(config_file)
year = config.get('mint', 'end_year')
region = config.get('mint', 'region')

# base dictionary
subsidies = {
    'year': year,
    'region': region,
    'crops': {}
}

# parsing economic files
for file in economic_files:
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['crop'] not in subsidies['crops']:
                subsidies['crops'][row['crop']] = {}
            crop = subsidies['crops'][row['crop']]
            subsidy = 'Fertilizer_Prices_No_Subsidy_%s' % year if row['fert_subsidy (%)'] == '0.00' else 'Fertilizer_Prices_%d_Subsidy_%s' % (float(row['fert_subsidy (%)']), year)
            crop[subsidy] = row['production (kg)']

# writing output file
with open(output_file, 'w') as f:
    writer = csv.writer(f)
    # write header
    header = ['year', 'region', 'crop']
    for value in subsidies['crops'].values():
        for key in value.keys():
            header.append(key)
        break
    writer.writerow(header)

    # write row
    for crop in subsidies['crops']:
        row = [subsidies['year'], subsidies['region'], crop]
        for key in subsidies['crops'][crop]:
            row.append(subsidies['crops'][crop][key])
        writer.writerow(row)
