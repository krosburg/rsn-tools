# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:08:51 2020

@author: Kellen
"""
# == IMPORTS ================================================================ #
import sys, json
from rsn_tools.core.playback import gaplist_from_file
from rsn_tools.core.engine import InstDataObj


# == FUNCTIONS FOR CLI INTERFACE ============================================ #
def print_help():
    print('USAGE: python status_check.py <gap_file>')
    print('  -h,--help   - Display this help message. Must be only argument.\n')


def get_args():
    nargs = len(sys.argv) - 1
    # Handle no arguments case
    if nargs < 1:
        print('Improper syntax!\n', file=sys.stderr)
        print_help()
        return None
    # Handle -h or --help arguments
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print_help()
        return None
    else:
        try:
            return sys.argv[1].split('=')[-1]
        except:
            return None


# == Main Program =========================================================== #
# Get CLI Arguments or Quit
cli_args = get_args()
if cli_args is None:
    quit()

# Read in Gap List
gap_list = gaplist_from_file(cli_args)

# Loop Through Reference Designators and Gaps
for refdes in gap_list.data:
    for gap in gap_list.data[refdes]:
        inst = InstDataObj(refdes)
        print('JOB ID: %i' % gap.job)
        try:
            inst.go(gap.start, gap.end, gap_list.server)
        except ValueError as err:
            print(err)
        print(json.dumps(inst.get_metadata_times(gap_list.server, stream='all'), indent=2))




                
                
                
                
                
                
                
                
                
                
                
                
                