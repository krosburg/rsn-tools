# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:08:51 2020

@author: Kellen
"""
# == IMPORTS ================================================================ #
import sys
sys.path.append("C:\\Users\\Kellen\\Code\\rsn-tools")
from core.engine import InstDataObj
from core.streams import rdList
from core.playback import gapListObj
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import numpy as np


# == FUNCTIONS FOR CLI INTERFACE ============================================ #
def nextItem(args, index):
    try:
        return args[index + 1], index + 1
    except IndexError:
        return None, index + 1


def print_help():
    print('USAGE: python rsn_gaps.py [options]')
    print('  -a,--all              - Use all reference designators. Ignores -r input. Must be ')
    print('                          first argument. Cannot be used with -r, -f, --refdes, or --file.\n')
    print('  -c,--check-only       - Do not run playback (find gaps only).\n')
    print('  -f <filename>         - Directs the program to read reference designators and times from')
    print('                          the file spcified by <filename>. Must be first argument. Cannot')
    print('                          be used with -r, -t, -a, --refes, --times, or --all.\n')
    print('  -f --help             - Displays file specific help w/ format and usage info.\n')
    print('  --file=<filename>     - Same as -f, but different syntax. Must be first argument. Cannot')
    print('                          be used with -r, -t, -a, --refes, --times, or --all.\n')
    print('  --file=help           - Displays file specific help w/ format and usage info.\n')
    print('  -h,--help             - Display this help message. Must be only argument.\n')
    print('  -r <rd1> <rd2>...     - Allows specification of reference designators to be used. -r is')
    print('                          followed by any number of reference designators separated by spaces.\n')
    print('  --refdes=<rd1>,<rd2>  - Same as -r, but reference designators are supplied in a comma separ-')
    print('                          ated list with no spaces.\n')
    print('  -s <dev03|dev01|prod> - Specifies playback server. If ommitted, dev03 is used by default. Ig-')
    print('                          nored if -c or --check-only is used.\n')
    print('  --server=<server>     - Same as -s.\n')
    print('  -t <t1> <t2>...       - Allows specification of time window starting times. Sytax same as -r.')
    print('  --times=<t1>,<t2>     - Same as -t, but time windows are supplied in a comma separated list')
    print('                          with no spaces.\n')
    

def print_file_help():
    print('USAGE: python rsn_gaps.py -f <filename>')
    print('       python rsn_gaps.py --file=<filename>\n')
    print('HELP:  python rsn_gaps.py -f --help')
    print('       python rsn_gaps.py --file=help\n')
    print('File format:')
    print('   [refdes]')
    print('   <refdes1>')
    print('   <refdes2>\n')
    print('   [times]')
    print('   <YYYY-MM>')
    print('   <YYYY-MM>\n')


def read_arg_file(filename):
    read_refdes = False
    read_times = False
    R = []
    T = []
    # Display File Help
    if filename == 'help' or filename == '--help':
        print_file_help()
        return [], []
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Sanitize
                line = line.split('\n')[0]
                if line.startswith('[refdes]'):
                    read_refdes = True
                    read_times = False
                elif line.startswith('[times]'):
                    read_refdes = False
                    read_times = True
                elif read_refdes:
                    if line[0:2] in ['CE', 'RS']:
                        R.append(line)
                elif read_times:
                    if int(line[0:4]) > 2003:
                        T.append(line)
    except FileNotFoundError:
        print('ERROR: Could not read file %s' % filename, file=sys.stderr)
    return R, T


def get_args_helper(ii):
    items = []
    arg, ii = nextItem(sys.argv, ii)
    while arg and not arg.startswith('-'):
        items.append(arg)
        arg, ii = nextItem(sys.argv, ii)
    return ii, items


def get_args():
    ii = 1
    nargs = len(sys.argv) - 1
    cabled_refdes = []
    time_windows = []
    allRD = False
    from_file = False
    want_playback = True
    server = 'dev03'
    # Handle no arguments case
    if nargs < 1:
        print('Improper syntax!\n', file=sys.stderr)
        print_help()
        return None
    # Handle -h or --help arguments
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print_help()
        return None
    if sys.argv[1] == '-a' or sys.argv[1] == '--all':
        cabled_refdes = [rd for rd in rdList]
        allRD = True
    if sys.argv[1] == '-f' and nargs > 1:
        cabled_refdes, time_windows = read_arg_file(sys.argv[2])
        from_file = True
        ii = 3
    if sys.argv[1].startswith('--file='):
        cabled_refdes, time_windows = read_arg_file(sys.argv[1].split('=')[-1])
        from_file = True
        ii = 2
    # Handle remaining arguments
    while ii < len(sys.argv):
        arg = sys.argv[ii]
        # Handle Refdes as "-r refdes refdes"
        if arg == '-r' and not allRD and not from_file:
            ii, cabled_refdes = get_args_helper(ii)
        # Handle time windows as "-t time time"
        elif arg == '-t' and not from_file:
            ii, time_windows = get_args_helper(ii)
        # Handle Refdes as "--refdes=rd,rd,rd"
        elif arg.startswith('--refdes=') and not allRD and not from_file:
            cabled_refdes = arg.split('=')[-1].split(',')
            arg, ii = nextItem(sys.argv, ii)
        # Handle Time Windows as "--times=time,time"
        elif arg.startswith('--times=') and not from_file:
            time_windows = arg.split('=')[-1].split(',')
            arg, ii = nextItem(sys.argv, ii)
        # Get the Check Only "-c" or "--check-only" argument
        elif arg == '-c' or arg == '--check-only':
            want_playback = False
            arg, ii = nextItem(sys.argv, ii)
        elif arg == '-s': 
            server, ii = nextItem(sys.argv, ii)
            arg, ii = nextItem(sys.argv, ii)
        elif arg == '--server':
            server = arg.split('=')[-1]
            arg, ii = nextItem(sys.argv, ii)
        # Ignore other arguments
        else:
            if arg not in ['-f', '-h', '-c', '-a', '--file', '--help', '--all', '--check-only']:
                print('Ignoring argument: ' + arg + '. See help (-h).')
            arg, ii = nextItem(sys.argv, ii)
    # Error Checking
    if not from_file:
        if len(cabled_refdes) == 0:
            print('Invalid syntax: no reference designators specified.', file=sys.stderr)
            return None
        if len(time_windows) == 0:
            print('Invalid syntax: no time windows specified.', file=sys.stderr)
            return None
        if want_playback and server not in ['prod', 'test', 'dev01', 'dev03']:
            print('Invalid syntax: no valid playback server specified.', file=sys.stderr)
            return None
    # Assemble Output
    return {'refdes': cabled_refdes,
            'times': time_windows,
            'pbflag': want_playback,
            'server': server}
    
    
# == VARIABLES FOR MAIN PROGRAM ============================================= #
# Cutoff and Time Vairables
cutoff_hours = 24
cutoff_frac = cutoff_hours/24.0
dt_cuttoff = timedelta(hours=cutoff_hours)
t_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
t_suffix = '-01T00:00:00.000Z'
                
                

# == FUNCTIONS FOR MAIN PROGRAM ============================================= #
def tConv(t):
    return mdates.num2date(t).replace(tzinfo=None)

def get_end_date(start_date):
    Y, M = start_date.split('-')
    if M == '12':
        return '%i-01' % (int(Y) + 1)
    return '%s-%02i' % (Y, int(M) + 1)

def build_window(start_date, t_suffix='-01T00:00:00.000Z'):
    """Defines the gap search window based on the start date."""
    return (start_date + t_suffix,
            get_end_date(start_date) + t_suffix)

def tPrint(t, tp_fmt='%Y-%m-%dT%H:%M:%S.000Z'):
    if type(t) is not datetime:
        t = tConv(t)
    return t.strftime(tp_fmt)

def find_gaps(rd, window_start):
    """Find gaps for a single refdes and time window. Returns list of tuples 
    containing gap start and end times [(start, end), ...]"""
    gaps = []
    SERVER = 'prod' # hard coded to search for gaps on production server
    # Get Window Start and End Times
    t_start, t_end = build_window(window_start)
    
    # Get Instrument Data and Metadata
    inst = InstDataObj(rd)
    inst.build_url(t_start, t_end, SERVER, DEBUG=False)
    metadata = inst.get_metadata_times(SERVER)[0]
    
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
            # Handle Delayed Start and Early End Plotting & Logging
            if bad_start:
                gaps.append((tPrint(dt_start), tPrint(t_i)))
            if bad_end:
                gaps.append((tPrint(t_f), tPrint(dt_end)))
                
            # Handle Mid-Secion Gaps
            if len(tbad) > 0:
                for j in range(len(tbad)-1):
                    gaps.append((tPrint(tbad[j]), tPrint(tbad[j+1])))
    # No data returned
    else:
        gaps.append(('', ''))
    return gaps


def build_gap_list(cabled_refdes, time_windows):
    gap_list = gapListObj()
    for refdes in cabled_refdes:
        for window in time_windows:
            for gap in find_gaps(refdes, window):
                gap_list.add(refdes, gap[0], gap[1])
    return gap_list



# == Main Program =========================================================== #
# Get CLI Arguments or Quit
cli_args = get_args()
if cli_args is None:
    quit()

# Server Selection Check
if cli_args['server'] == 'prod':
    pmesg = '\n== WARNING ================================================\n'
    pmesg += ' Hey buddy...\n You set playback server to PRODUCTION...\n'
    pmesg += '\n Are you sure you want to do that? [yes/n]: '
    if input(pmesg).lower() != 'yes':
        print("\nGood. I didn't think so. Aborting.")
        quit()
    else:
        print('\nYour call... Carrying on (but not keeping calm).\n')
    
    
# Create the list of gaps
gap_list = build_gap_list(cli_args['refdes'], cli_args['times'])

msg = '\n\nrsn_gaps.py will run on reference designators'
if cli_args['refdes'] is None and cli_args['times'] is None:
    msg += ' read from the specified file,\n'
else:
    msg += ':\n' + '\n'.join(cli_args['refdes']) + '.\n'
msg += 'using times'
if cli_args['refdes'] is None and cli_args['times'] is None:
    msg += ' read from the specified file.\n'
else:
    msg += ':\n' + '\n'.join(cli_args['times']) + '.\n'
msg += 'Gaps will'
if not cli_args['pbflag']:
    msg += ' not'
msg += ' be played back'
if cli_args['pbflag']:
    msg += ' on ' + cli_args['server']
msg += '.'

print(msg)

gap_list.dump()

                
                
                
                
                
                
                
                
                
                
                
                
                
                