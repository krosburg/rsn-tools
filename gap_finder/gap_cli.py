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
cutoff_hours = 24
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
        print(rd)
    
    # Get Start and End dates
    if sys.argv[2][0:4].isnumeric() and sys.argv[3][0:4].isnumeric():
        print("here")
        t_start = sys.argv[2] + t_suffix
        print(t_start)
        t_end = sys.argv[3] + t_suffix
        print(t_end)
    else:
        useErr()
        
    # Get Logfile
    if not sys.argv[4].isnumeric():
        log_path = sys.argv[4]
        print(log_path)
        if not log_path.endswith('/'):
            log_path += '/'
        f = open(log_path + rd + '_' + sys.argv[2] + '.log', 'w+')
    else:
        useErr()

# Instantiate Instrument Object
inst = InstDataObj(rd)
  
# Run Data Check & Plot if data come back
inst.build_url(t_start, t_end, SERVER, DEBUG=False)
if inst.get_data(SERVER):
    # Convert Time Data to Datetime Format
    t_i = tConv(inst.t[0])
    t_f = tConv(inst.t[-1])
    dt_start = datetime.strptime(t_start, t_fmt)
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
    
    # Handle Delayed Start and Early End Plotting & Logging
    if bad_start:
        f.write("%s to %s (start gap)\n" % (tPrint(dt_start), tPrint(t_i)))
    if bad_end:
        f.write("%s to %s (end gap)\n" % (tPrint(t_f), tPrint(dt_end)))
        
    # Handle Mid-Secion Gaps
    if len(tbad) > 0:
        for j in range(len(tbad)-1):
            f.write("%s to %s\n (middle gap)" % (tPrint(tbad[j]), tPrint(tbad[j+1])))
        
f.close()
       
