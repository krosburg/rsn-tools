# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 11:56:06 2020
@author: K.C. Rosburg, UW/APL/RSN

This script generates a shell script with a bunch of rsn-tools.gap_finder.gap_cli.py
commands for the specified reference designators and times. Times are specified
by the times variable, which for the most part doesn't need to be touched.
Other user variables can be modified in the user variable section. The refdes
will be tacked on to BASE_PATH and a folder will be created for that refdes if
MAKE_DIRS=True. If the refdes list RDS is left empty, the rsn-tools.core.streams
pre-defined list of all refdes' will be used. CMD_FILE designates the output of
this script.
"""
import sys, os
sys.path.append("C:\\Users\\Kellen\\Code\\rsn-tools")
from core.streams import rdList
times = ['2014-08', '2014-09', '2014-10', '2014-11', '2014-12', '2015-01',
         '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', '2015-07',
         '2015-08', '2015-09', '2015-10', '2015-11', '2015-12', '2016-01',
         '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07',
         '2016-08', '2016-09', '2016-10', '2016-11', '2016-12', '2017-01',
         '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07',
         '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01',
         '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07',
         '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01',
         '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07',
         '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01']


# == USER VARIABLES ========================================================= #
# Path that gap_cli.py should write gap logs to
BASE_PATH = './logs/'

# Reference designator list to process
#   (Leave blank to use full rdList from rsn-tools.core.streams)
RDS = []

# Where to save the command file
CMD_FILE = './bulk_cli_cmds.sh'

# Should I Create Directories?
MAKE_DIRS = True
#MAKE_DIRS = False
# =========================================================================== #


# == MAIN PROGRAM =========================================================== #
# Determine which list to use
if len(RDS) == 0:
    RDS = rdList

# Open File
f = open(CMD_FILE, 'w+')

# Loop on RefDes
for rd in RDS:
    if not BASE_PATH.endswith('/'):
        BASE_PATH += '/'
    log_path = BASE_PATH + rd + '/'
    
    # Create Directories
    if MAKE_DIRS:
        try:
            os.makedirs(log_path, exist_ok=True)
        except OSError as e:
            print("Creation of the directory " + log_path + " failed")
        else:
            print("Created directory " + log_path)

    # Loop on Dates
    for ii in range(len(times)-1):
        f.write('python gap_cli.py %s %s %s %s\n' % (rd,
                                                     times[ii],
                                                     times[ii+1],
                                                     log_path))
    # Put a separator between ref-des blocks
    f.write('\n')
    
# Close File
f.close()