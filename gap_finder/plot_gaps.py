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
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np



# == FUNCTION DEFINITIONS =================================================== #
def tConv(t):
    return mdates.num2date(t).replace(tzinfo=None)

def tPrint(t, tp_fmt='%Y-%m-%dT%H:%M:%SZ'):
    if type(t) is not datetime:
        t = tConv(t)
    return t.strftime(tp_fmt)
    

# == MAIN PROGRAM =========================================================== #
# User Variables
LOGFILE = 'C:/Users/Kellen/Desktop/tmp/logs'
SERVER = 'prod'
t_start = '2016-12-01T00:00:00.000Z'
t_end = '2017-01-01T00:00:00.000Z'
rd = 'CE04OSPS-PC01B-4D-PCO2WA105'
times = ['2018-07', '2018-08', '2018-09', '2018-10']#['2014-08', '2014-09', '2014-10', '2014-11', '2014-12', '2015-01',
        # '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', '2015-07',
        # '2015-08', '2015-09', '2015-10', '2015-11', '2015-12', '2016-01',
        # '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07',
        # '2016-08', '2016-09', '2016-10', '2016-11', '2016-12', '2017-01',
        # '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07',
        # '2017-08', '2017-09', '2017-10', '2017-11', '2017-12', '2018-01',
        # '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07',
        # '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01',
        # '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07',
        # '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01']

# Cutoff and Time Vairables
cutoff_hours = 24
cutoff_frac = cutoff_hours/24.0
dt_cuttoff = timedelta(hours=cutoff_hours)
t_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
t_suffix = '-01T00:00:00.000Z'


# Loop Through All Times
for ii in range(len(times)-1):
    # Setup Time Range
    t_start = times[ii] + t_suffix
    t_end = times[ii+1] + t_suffix
    
    # Instantiate Instrument Object
    inst = InstDataObj(rd)
      
    # Run Data Check & Plot if data come back
    inst.build_url(t_start, t_end, SERVER, DEBUG=False)
    if inst.get_data(SERVER):
        # Convert Time Data to Datetime Format
        t_i = tConv(inst.t[0]) #mdates.num2date(inst.t[0]).replace(tzinfo=None)
        t_f = tConv(inst.t[-1]) # mdates.num2date(inst.t[-1]).replace(tzinfo=None)
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
        
        # Print Header for Missing Data (if exists)
        if tbad.size > 0 or bad_start or bad_end:
            print("MISSING DATA!!!")
            print('The following points had a time gradient exceeding %d hours:' % cutoff_hours)
        
        # Plot Gradient + Bad Points
        plt.figure(figsize=(15,4))
        plt.plot(inst.t, np.gradient(inst.t), '.')
        plt.plot(tbad, tgradbad, 'or')
        
        # Plot Limits and Date Formatting
        ax1 = plt.gca()
        plt.xlim([dt_start, dt_end])
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%m/%d/%y'))
        
        # Handle Delayed Start and Early End Plotting & Logging
        ytop = 1.0
        if np.nanmax(tgrad) > ytop:
            ytop = np.nanmax(tgrad)
        ymid = 0.5 * ytop
        if bad_start:
            plt.plot([t_i, t_i], [0, ytop], '-r')
            plt.plot([dt_start, dt_start], [0, ytop], '-r')
            plt.plot([dt_start, t_i], [ymid, ymid], '-r')
            print("   %s to %s" % (tPrint(dt_start), tPrint(t_i)))
        if bad_end:
            plt.plot([t_f, t_f], [0, ytop], '-r')
            plt.plot([dt_end, dt_end], [0, ytop], '-r')
            plt.plot([t_f, dt_end], [ymid, ymid], '-r')
            print("   %s to %s" % (tPrint(t_f), tPrint(dt_end)))
            
        # Handle Mid-Secion Gaps
        for j in range(len(tbad)-1):
            plt.plot([tbad[j], tbad[j]], [0, ytop], '-r')
            plt.plot([tbad[j+1], tbad[j+1]], [0, ytop], '-r')
            plt.plot([tbad[j], tbad[j+1]], [ymid, ymid], '-r')
            print("   %s to %s" % (tPrint(tbad[j]), tPrint(tbad[j+1])))
            
        # Plot Lables and CLeanup
        plt.title("%s - %s to %s" % (inst.ref_des, t_start[0:10], t_end[0:10]))
        plt.ylabel('Time Gradient (days)')
        plt.grid()
        plt.show()
        print('\n')
        
       
