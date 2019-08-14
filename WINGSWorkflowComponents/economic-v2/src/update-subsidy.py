#!/usr/bin/env python

import csv
import sys
import tempfile
from shutil import copyfile

subsidy_file = sys.argv[1]
subsidy = float(sys.argv[2])
temp_file = tempfile.mkstemp()

with open(subsidy_file, 'rb') as f:
    with open(temp_file[1], 'wb') as fo:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(fo, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            row['c2'] = str(float(row['c2']) * subsidy)
            writer.writerow(row)

copyfile(temp_file[1], subsidy_file)

