# Gap Finder
## Summary
A collection of scripts used to help identify data gaps. These scripts rely on the `rsn-tools.core` package.

## gap_cli.py
### Description
`gap_cli.py` is a command line tool used to check for data gaps for a single given reference designator (RD) and single given time range identified by a start and end year-month combination (i.e. yyyy-mm; see Usage below). The tool writes to a log file in the given log directory.

The tool will detect any datagaps larger than `cutoff_hours` (default 24 hr). This can be modified within the code if you dare. It will also detect beginning end gaps, i.e. gaps that begin/end outside of the user specified time range. If those gaps are due to the user specified time range being outside of the M2M data start or data end times for that instrument, the gap will be ignored as a false gap (because it is). If the start time of a user specified time range starts before the M2M data start time for an instrument, the user start time will be changed to the metadata start time to avoid a false gap. The same is true for end times. Note that this has the potential to miss real data gaps in a situation where an instrument was producing data prior to the M2M metadata beginTime, but for which data had not yet been playedback.

The tool is intended to be run by a cronjob on a monthly basis to monitor and update a repository of data gaps. Because of this the 24 hour cutoff only works well if the spacing between data points is less than 24 hours. It is recommended to only use 1-month long user specified data ranges. A bulk tool is in the works for checking a large amount of data. This tool will generate a shell script with many gap_cli commands to be run sequentially.

### Usage
Basic useage: `python gap_cli.py <reference-designator> <start> <end> <log-file-directory>`

Detailed usage: needs to be written

### Installation
1. Create a Python 3.6+ Conda or Pip environment with numpy, requests, pandas, urllib3, datetime, matplotlib, sys, and os (some of these may be included by default)
1. Clone the git repository into a directory of your choosing
1. Find all python files that contain a `sys.path.append` line in the imports section and change the file path to `/your/install/dir/rsn-tools/`
1. Activate your environment
1. You should be able to run the code now.


## plot_gaps.py
### Description
Description is needed.
