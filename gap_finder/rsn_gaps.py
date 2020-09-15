# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:08:51 2020

@author: Kellen
"""
# == IMPORTS ================================================================ #
import sys, json, os
from rsn_tools.core.engine import InstDataObj
from rsn_tools.core.streams import rdList
from rsn_tools.core.playback import gapListObj, bulk_playback, gaplist_from_file
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
    print('  --force               - Sets checkExistingFiles to False to force playback of datalogs.\n')
    print('  -h,--help             - Display this help message. Must be only argument.\n')
    print('  --no-log              - Disables writing of gap log file for testing, etc.\n')
    print('  --log-path=<path>     - Sets the path to write log file (path only, filename is set auto-')
    print('                          matically; e.g: "/home/logs/"). If not set, uses current directory.\n')
    print('  --preview             - Displays preview playback requests without submitting them.\n')
    print('  -r <rd1> <rd2>...     - Allows specification of reference designators to be used. -r is')
    print('                          followed by any number of reference designators separated by spaces.\n')
    print('  --refdes=<rd1>,<rd2>  - Same as -r, but reference designators are supplied in a comma separ-')
    print('                          ated list with no spaces.\n')
    print('  --resume=<gapfile>    - Starts playback from a gapfile. The gapfile must be a file dumped in')
    print('                          gap_list format by this program. This option will automatically kick')
    print('                          off playback for all gaps in the log on dev03, unless the server')
    print('                          is defined with the -s or --server= flags.\n')
    print('  -s <dev03|dev01|prod> - Specifies playback server. If ommitted, dev03 is used by default. Ig-')
    print('                          nored if -c or --check-only is used.\n')
    print('  --server=<server>     - Same as -s.\n')
    print('  -t <t1> <t2>...       - Allows specification of time window starting times. Sytax same as -r.')
    print('  --times=<t1>,<t2>     - Same as -t, but time windows are supplied in a comma separated list')
    print('                          with no spaces.\n')
    quit()
    

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
    quit()


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
    want_gaps = True
    server = 'dev03'
    logpath = '.'
    gapfile = None
    preview_only = False
    logging = True
    force = False
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
    if sys.argv[1].startswith('--resume='):
        gapfile = sys.argv[1].split('=')[-1]
        want_gaps = False
        ii = 2
    # Handle remaining arguments
    while ii < len(sys.argv):
        arg = sys.argv[ii]
        # Handle Refdes as "-r refdes refdes"
        if arg == '-r' and not allRD and not from_file and want_gaps:
            ii, cabled_refdes = get_args_helper(ii)
        # Handle time windows as "-t time time"
        elif arg == '-t' and not from_file and want_gaps:
            ii, time_windows = get_args_helper(ii)
        # Handle Refdes as "--refdes=rd,rd,rd"
        elif arg.startswith('--refdes=') and not allRD and not from_file and want_gaps:
            cabled_refdes = arg.split('=')[-1].split(',')
            arg, ii = nextItem(sys.argv, ii)
        # Handle Time Windows as "--times=time,time"
        elif arg.startswith('--times=') and not from_file and want_gaps:
            time_windows = arg.split('=')[-1].split(',')
            arg, ii = nextItem(sys.argv, ii)
        # Get the Check Only "-c" or "--check-only" argument
        elif arg == '-c' or arg == '--check-only' and want_gaps:
            want_playback = False
            arg, ii = nextItem(sys.argv, ii)
        elif arg == '-s': 
            server, ii = nextItem(sys.argv, ii)
            arg, ii = nextItem(sys.argv, ii)
        elif arg.startswith('--server'):
            server = arg.split('=')[-1]
            arg, ii = nextItem(sys.argv, ii)
        elif arg.startswith('--log-path='):
            logpath = arg.split('=')[-1]
            os.makedirs(logpath, exist_ok=True)
            arg, ii = nextItem(sys.argv, ii)
        elif arg == '--preview':
            preview_only = True
            arg, ii = nextItem(sys.argv, ii)
        elif arg == '--force' and want_playback:
            force = True
            arg, ii = nextItem(sys.argv, ii)
        elif arg == '--no-log':
            logging = False
            arg, ii = nextItem(sys.argv, ii)
        # Ignore other arguments
        else:
            if arg not in ['-f', '-h', '-c', '-a', '--file', '--help', '--all', '--check-only']:
                print('Ignoring argument: ' + arg + '. See help (-h).')
            arg, ii = nextItem(sys.argv, ii)
    # Error Checking
    if not from_file:
        if len(cabled_refdes) == 0 and gapfile is None:
            print('Invalid syntax: no reference designators specified.', file=sys.stderr)
            return None
        if len(time_windows) == 0 and gapfile is None:
            print('Invalid syntax: no time windows specified.', file=sys.stderr)
            return None
        if want_playback and server not in ['prod', 'test', 'dev01', 'dev03']:
            print('Invalid syntax: no valid playback server specified.', file=sys.stderr)
            return None
    # Assemble Output
    return {'refdes': cabled_refdes,
            'times': time_windows,
            'pbflag': want_playback,
            'gapflag': want_gaps,
            'logpath': logpath,
            'gapfile': gapfile,
            'server': server,
            'preview': preview_only,
            'logging': logging,
            'force': force}
    
    
# == VARIABLES FOR MAIN PROGRAM ============================================= #
# Cutoff and Time Vairables
cutoff_hours = 24
#cutoff_hours = 6
cutoff_frac = cutoff_hours/24.0
dt_cuttoff = timedelta(hours=cutoff_hours)
t_fmt = '%Y-%m-%dT%H:%M:%S.%fZ'
t_suffix = '-01T00:00:00.000Z'
run_date = datetime.utcnow()
logfile = 'rsn_gaplist_' + run_date.strftime('%Y-%m-%dT%H_%MZ') + '.log'
                
                

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
        try:
            tgrad = np.gradient(inst.t)
        except ValueError as err:
            print(err)
            gaps.append(('', ''))
            return gaps

        tbad = inst.t[tgrad >= cutoff_frac]
        tgradbad = tgrad[tgrad >= cutoff_frac]
    
        # Open file if gaps
        if bad_start or bad_end or len(tbad) > 0:        
            # Handle Delayed Start
            if bad_start:
                gaps.append((tPrint(dt_start), tPrint(t_i)))
                
            # Handle Mid-Secion Gaps
            if len(tbad) > 0:
                for j in range(len(tbad)-1):
                    gaps.append((tPrint(tbad[j]), tPrint(tbad[j+1])))
            
            #  Handle Early End
            if bad_end:
                gaps.append((tPrint(t_f), tPrint(dt_end)))
                
            
    # No data returned
    else:
        gaps.append(('', ''))
    return gaps


def build_gap_list(cabled_refdes, time_windows):
    gap_list = gapListObj(server=cli_args['server'])
    for refdes in cabled_refdes:
        for window in time_windows:
            for gap in find_gaps(refdes, window):
                gap_list.add(refdes, gap[0], gap[1])
    return gap_list


def dump_log_file(logpath, logfile):
    outfile = '/'.join([logpath, logfile])
    cnt = 0
    fh = None
    # Create File Handle / Open For Writing
    while fh is None:
        try:
            fh = open(outfile, 'x')
        except:
            if cnt < 1:
                outfile += '.' + str(cnt)
            else:
                outfile = outfile[:-1] + str(cnt)
            cnt += 1
        if cnt > 5:
            raise('ERROR: Could not create log file!')
    # Write to Log and Close File
    fh.write(json.dumps({'gap_list': gap_list.dump('JSON'),
                         'run_info':
                             {'run_date': run_date.isoformat(),
                              'command': ' '.join(sys.argv),
                              'refdes': cli_args['refdes'],
                              'times': cli_args['times'],
                              'server': cli_args['server']}
                             },
                             indent=2))
    fh.close()
    
    
def update_log_file(logfile):
    # Create File Handle / Open For Writing  
    fh = open(logfile, 'w')
    # Write to Log and Close File
    fh.write(json.dumps({'gap_list': gap_list.dump('JSON'),
                         'run_info':
                             {'run_date': run_date.isoformat(),
                              'command': ' '.join(sys.argv),
                              'refdes': cli_args['refdes'],
                              'times': cli_args['times'],
                              'server': cli_args['server']}
                             },
                             indent=2))
    fh.close()


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
if cli_args['gapflag']:
    print('Building gaps from scratch')
    # Check Refdes for Accuracy
    for refdes in cli_args['refdes']:
        if refdes not in rdList:
            raise('ERROR: Invalid reference desigantor. Check your input! Aborting.')
    gap_list = build_gap_list(cli_args['refdes'], cli_args['times'])
elif cli_args['gapfile'] is not None and cli_args['pbflag']:
    print('Loading gaps from file')
    gap_list = gaplist_from_file(cli_args['gapfile'])

gap_list.dump()
print('\n======================================================================')
print('%s,%30s,%22s' % ('Refdes', 'Gap Start', 'Gap End'))
for rd in gap_list.data:
    for gap in gap_list.data[rd]:
        print('%s,%s,%s' % (gap.refdes, gap.start, gap.end) )
print('======================================================================\n')

# Add playback bit here
if cli_args['pbflag']:
    print('Playing back!')
    gap_list.dump()
    bulk_playback(cli_args['server'], gap_list, preview_only=cli_args['preview'], force=cli_args['force'], DEBUG=False)

# Dump to Log
if not cli_args['preview'] and cli_args['logging']:
    # Logfile updates
    if cli_args['gapfile'] is not None:
        print('Updating logfile: ' + cli_args['gapfile'])
        update_log_file(cli_args['gapfile'])
    # Log file creation
    else:
        print('Writing logfile: ' + '/'.join([cli_args['logpath'], logfile]))
        dump_log_file(cli_args['logpath'], logfile)
elif cli_args['preview']:
    print('WARNING: preview mode enabled. Bypassing logfile dump.')
elif not cli_args['logging']:
    print('WARNING: Logging disabled. Bypassing logfile dump.')






                
                
                
                
                
                
                
                
                
                
                
                
                