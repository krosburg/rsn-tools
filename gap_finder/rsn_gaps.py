# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:08:51 2020

@author: Kellen
"""
# == IMPORTS ================================================================ #
import sys
sys.path.append("C:\\Users\\Kellen\\Code\\rsn-tools")
from core.streams import rdList


def nextItem(args, index):
    try:
        return args[index + 1], index + 1
    except IndexError:
        return None, index + 1

# TODO: Finish this
def print_help():
    print('USAGE: python rsn_gaps.py [options]')
    print('  -a,--all             - Use all reference designators. Ignores -r input. Must be ')
    print('                         first argument. Cannot be used with -r, -f, --refdes, or --file.\n')
    print('  -c,--check-only      - Do not run playback (find gaps only).\n')
    print('  -f <filename>        - Directs the program to read reference designators and times from')
    print('                         the file spcified by <filename>. Must be first argument. Cannot')
    print('                         be used with -r, -t, -a, --refes, --times, or --all.\n')
    print('  --file=<filename>    - Same as -f, but different syntax. Must be first argument. Cannot')
    print('                         be used with -r, -t, -a, --refes, --times, or --all.\n')
    print('  -h,--help            - Display this help message. Must be only argument.\n')
    print('  -r <rd1> <rd2>...    - Allows specification of reference designators to be used. -r is')
    print('                         followed by any number of reference designators separated by spaces.\n')
    print('  --refdes=<rd1>,<rd2> - Same as -r, but reference designators are supplied in a comma separ-')
    print('                         ated list with no spaces.\n')
    print('  -t <t1> <t2>...       - Allows specification of time window starting times. Sytax same as -r.')
    print('  --times=<t1>,<t2>     - Same as -t, but time windows are supplied in a comma separated list')
    print('                          with no spaces.\n')
    
# TODO: Finish this
def read_arg_file(filename):
    print('Not yet implemented reading from file: ' + filename)
    return None, None


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
    # Handle no arguments case
    if nargs < 1:
        print('Improper syntax!\n')
        print_help()
        return 1
    # Handle -h or --help arguments
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print_help()
        return 0
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
        # Ignore other arguments
        else:
            if arg not in ['-f', '-h', '-c', '-a', '--file', '--help', '--all', '--check-only']:
                print('Ignoring argument: ' + arg + '. See help (-h).')
            arg, ii = nextItem(sys.argv, ii)
    # Error Checking
    if not from_file:
        if len(cabled_refdes) == 0:
            print('Invalid syntax: no reference designators specified.')
            return 1
        if len(time_windows) == 0:
            print('Invalid syntax: no time windows specified.')
            return 1
    # Assemble Output
    return {'refdes': cabled_refdes,
            'times': time_windows,
            'pbflag': want_playback}
                
                


# Main Program
cli_args = get_args()

if cli_args != 1:
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
    msg += ' be played back.'
    
    print(msg)

                
                
                
                
                
                
                
                
                
                
                
                
                
                