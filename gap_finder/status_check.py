# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 12:08:51 2020

@author: Kellen
"""
# == IMPORTS ================================================================ #
import sys
sys.path.append("C:\\Users\\Kellen\\Code\\rsn-tools")
from core.playback import gaplist_from_file


# == FUNCTIONS FOR CLI INTERFACE ============================================ #
def nextItem(args, index):
    try:
        return args[index + 1], index + 1
    except IndexError:
        return None, index + 1


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

gap_list = gaplist_from_file(cli_args)
gap_list.status()    
    







                
                
                
                
                
                
                
                
                
                
                
                
                