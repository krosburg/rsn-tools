# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:08:51 2020

@author: Kellen
"""
# == IMPORTS ================================================================ #
import sys
sys.path.append("C:\\Users\\Kellen\\Code\\rsn-tools")
from core.engine import InstDataObj
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np



# == FUNCTION DEFINITIONS =================================================== #
def tConv(t):
    return mdates.num2date(t).replace(tzinfo=None)

def tPrint(t, tp_fmt='%Y-%m-%dT%H:%M:%SZ'):
    if type(t) is not datetime:
        t = tConv(t)
    return t.strftime(tp_fmt)

def useErr():
    print("ERROR! Usage: python <prgm-name> <ref-des> <start month-date> <end month-date> <log-file>")
    print("              (e.g: python test_gapping.py CE04OSPS-PC01B-4D-PCO2WA105 2018-07 2018-08 ./log.txt)")
    quit()
    

# == MAIN PROGRAM =========================================================== #
# User Variables
SERVER = 'prod'

# Cutoff and Time Vairables
cutoff_hours = 6
cutoff_frac = cutoff_hours/24.0
dt_cuttoff = timedelta(hours=cutoff_hours)
t_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
t_suffix = '-01T00:00:00.000Z'

# Process CLI Arguments
nargs = len(sys.argv) - 1
if nargs < 4:
    useErr()
else:
    # Get reference designator
    if sys.argv[1].isnumeric():
        raise Exception('ERROR: Invalid refdes')
    else:
        rd = sys.argv[1]
    
    # Get Start and End dates
    if sys.argv[2][0:4].isnumeric() and sys.argv[3][0:4].isnumeric():
        t_start = sys.argv[2] + t_suffix
        t_end = sys.argv[3] + t_suffix
    else:
        useErr()
        
    # Get Logfile
    if not sys.argv[4].isnumeric():
        log_path = sys.argv[4]
        if not log_path.endswith('/'):
            log_path += '/'
        log_file = rd + '_' + sys.argv[2] + '.log'
    else:
        useErr()

# Instantiate Instrument Object
inst = InstDataObj(rd)
inst.build_url(t_start, t_end, SERVER, DEBUG=False)

# t_start,t_end are the time window start and ends
# t_i, t_f are the dataset start & end times



# Get Metadata/Times Bounds & Check 
metadata = inst.get_metadata_times(SERVER)
  
# Run Data Check & Plot if data come back
if t_end < metadata['beginTime'] or t_start > metadata['endTime']:
    print('Given time range is outside data bounds - SKIPPING!')
elif inst.get_data(SERVER):
    # Convert Time Data to Datetime Format
    t_i = tConv(inst.t[0])
    t_f = tConv(inst.t[-1])
    if t_start < metadata['beginTime']:
        dt_start = datetime.strptime(metadata['beginTime'], t_fmt)
    else:
        dt_start = datetime.strptime(t_start, t_fmt)
    if t_end > metadata['endTime']:
        dt_end = datetime.strptime(metadata['endTime'], t_fmt)
    else:
        dt_end = datetime.strptime(t_end, t_fmt)

    
    # Bulk Start/End Checks
    bad_start, bad_end = False, False
    if t_i >= dt_start + dt_cuttoff:
        bad_start = True
    if t_f <= dt_end - dt_cuttoff:
        bad_end = True
    
    # Take Gradient and Find Bad Points
    tgrad = np.gradient(inst.t)
    tbad = inst.t[tgrad >= cutoff_frac]
    tgradbad = tgrad[tgrad >= cutoff_frac]
    
    # Open file if gaps
    if bad_start or bad_end or len(tbad) > 0:
        print("Writing to log: " + log_path + log_file + "...", end="")
        try:
            f = open(log_path + log_file, 'w+')
        except:
            print(' FAIL!')
            raise Exception('ERROR: Could not open/write file!')
    
        # Handle Delayed Start and Early End Plotting & Logging
        if bad_start:
            f.write("%s to %s (start gap)\n" % (tPrint(dt_start), tPrint(t_i)))
        if bad_end:
            f.write("%s to %s (end gap)\n" % (tPrint(t_f), tPrint(dt_end)))
            
        # Handle Mid-Secion Gaps
        if len(tbad) > 0:
            for j in range(len(tbad)-1):
                f.write("%s to %s (middle gap)\n" % (tPrint(tbad[j]), tPrint(tbad[j+1])))
        print(" Done!")
        
        # Close FIle
        print('Closing log file...', end='')
        f.close()
        print(" Done!")
    
    else:
        print("No gaps: no log file created.")

# No data returned
else:
    print("Writing to log: " + log_path + log_file + "...", end="")
    try:
        f = open(log_path + log_file, 'w+')
    except:
        print(' FAIL!')
        raise Exception('ERROR: Could not open/write file!')
    f.write("No data returned from M2M. This could mean the time range\n")
    f.write("contains no data, the request timed out, or another error\n")
    f.write("occured.")
    print(' Done!')
    
    # Close FIle
    print('Closing log file...', end='')
    f.close()
    print(" Done!")

# Final line skip
print('')

