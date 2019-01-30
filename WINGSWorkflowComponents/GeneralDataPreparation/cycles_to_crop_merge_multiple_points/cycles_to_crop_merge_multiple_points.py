#!/usr/bin/env python3

import csv
import sys

csv_columns = ['', 'ybarN']
data = []

for file in sys.argv[1:-1]:
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            crop = row['']
            value = row['ybarN']
            if any(crop == d[''] for d in data):
                for d in data:
                    if float(d['ybarN']) == -99:
                        d['ybarN'] = value
                        break
            else:
                data.append({'': crop, 'ybarN': value})

# write merged crop yield
csv_file = sys.argv[-1:][0]
with open(csv_file, 'w') as f:
    w = csv.DictWriter(f, fieldnames=csv_columns)
    w.writeheader()
    for d in data:
        w.writerow(d)
