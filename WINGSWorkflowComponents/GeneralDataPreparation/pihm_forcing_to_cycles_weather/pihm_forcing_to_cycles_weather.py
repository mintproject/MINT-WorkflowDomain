#!/usr/bin/env python3

import datetime
import math
import subprocess
import sys
import csv

from dateutil import parser


def find_day_entry(forcing_file, index, variable, day):
    with open(forcing_file) as ffile:
        found_block = False
        for line in ffile:
            if line.startswith(variable + ' ' + str(index) + ' '):
                found_block = True
            if found_block and line.startswith(str(day) + ' '):
                return float(line.split()[1])


def satvp(temp):
    return .6108 * math.exp(17.27 * temp / (temp + 237.3))


def tdew(ea):
    return 237.3 * math.log(ea / 0.6108) / (17.27 - math.log(ea / 0.6108))


def ea(patm, q):
    return patm * q / (0.622 * (1 - q) + q)


def process_day(forcing_file, index, dt):
    '''
    process one day of PIHM Forcing data and convert it to Cycles input
    '''
    day = dt.timetuple().tm_yday - 1
    tavg = find_day_entry(forcing_file, index, 'Temp', day)
    rH = find_day_entry(forcing_file, index, 'RH', day)
    ea_kPa = rH * satvp(tavg)

    delta_T = 17.37 * (1.01 - 1 / (1 + 3 * (1/rH - 1)))
    Tdew = tdew(ea_kPa)

    pp = find_day_entry(forcing_file, index, 'Precip', day) * 1000
    tx = tavg + .5 * delta_T
    tn = tavg - .5 * delta_T
    solar =  find_day_entry(forcing_file, index, 'RN', day) / 1000000
    if tn > Tdew:
        rhx = 100 * ea_kPa / satvp(tn)
    else:
        rhx = 99.9
    if tx > Tdew:
        rhn = 100 * ea_kPa / satvp(tx)
    else:
        rhn = 99.8
    wind = find_day_entry(forcing_file, index, 'Wind', day) / 86400

    data = '%s  %6.2f  %6.2f  %6.2f  %8.4f  %8.4f %8.4f %6.2f\n' \
           %(dt.strftime('%Y  %j'), pp, tx, tn, solar, rhx, rhn, wind)

    return (data, 0)


def main():
    forcing_file = sys.argv[1]
    attribute_file = sys.argv[2]
    cropland_file = sys.argv[3]
    # start and end dates
    start_dt = parser.parse(sys.argv[4] + 'T00:00:00')
    end_dt = parser.parse(sys.argv[5] + '-T23:59:59')
    weather_file = sys.argv[6]

    # TEMP: counter
    count = 0

    with open(cropland_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if count == 1:
                break
            count += 1
            cell_index = int(row['SP_ID'])
            lat = float(row['Y_c'])
            lon = float(row['X_c'])
            elevation = float(row['Zmax']) - float(row['Zmin'])

            with open(attribute_file) as att_file:
                for line in att_file:
                    if line.startswith(str(cell_index) + '\t'):
                        index = int(line.split()[9])
                        break

            # now extract daily values for the time range
            data = ""
            Patm_total = 0.0
            Patm_count = 0
            dt = start_dt
            while dt <= end_dt:
                (line, Patm) = process_day(forcing_file, index, dt)
                data += line
                Patm_total += Patm
                Patm_count += 1
                # move on to the next day
                dt = dt + datetime.timedelta(days = 1)

            fname = weather_file
            fp = open(fname, 'w')
            fp.write('LATITUDE %.2f\n' %float(lat))
            fp.write('ALTITUDE %.2f\n' %(elevation))
            fp.write('SCREENING_HEIGHT 2\n')
            fp.write('YEAR  DOY     PP      TX      TN     SOLAR      RHX      RHN     WIND\n')
            fp.write(data)
            fp.close()

main()
