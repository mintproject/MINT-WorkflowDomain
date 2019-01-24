#!/usr/bin/env python3

import configparser
import glob
import datetime
import os
import subprocess
import sys
import re


def my_cmd(cmd):
    print()
    print(cmd)
    exit_code = subprocess.call(cmd, shell=True)
    if exit_code != 0:
        print('Command failed with exit code %d' %(exit_code))
        sys.exit(1)


def main():

    # get the general configuration from the global mint_run.config
    run_config = configparser.ConfigParser()
    run_config.read(sys.argv[1])

    start_year = run_config.get('mint', 'start_year')
    end_year = run_config.get('mint', 'end_year')

    start_date = datetime.date(int(start_year), 1, 1)
    end_date = datetime.date(int(end_year), 12, 31)
    delta = end_date - start_date
    duration_mins = delta.days * 24 * 60
    
    # determine project name
    os.chdir('PIHM-base')
    project_name = glob.glob('*.para')
    if len(project_name) != 1:
        print('Unable to determine project name!')
        sys.exit(1)
    project_name = project_name[0]
    project_name = re.sub('\.para', '', project_name)

    # run the model
    my_cmd('/usr/bin/pihm ' + project_name + ' 2>&1')


main()

