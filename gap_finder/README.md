# Gap Finder
## Summary
A collection of scripts used to help identify data gaps. These scripts rely on the `rsn-tools.core` package.

## rsn_gaps.py - Main Program
### Description
`rsn_gaps.py` is a command line tool used to identify data gaps on the OOI UFRAME/M2M system. This tool has many options and therefore is faily versitile. It can both identify gaps for one or more reference designators and start playback for those gaps on any of the OOINet servers (given appropriate credentials). At present, gaps are defined as a period of 24 hours or more without data and are detected using a simple gradent on the time variable returned by M2M. The option to change the gap duration is planned for a future release.

Detected gaps, run parameters, and any associated playback information is saved to a gap log file (JSON format) at each run of `rsn_gaps.py`, unless the `--preview` or `--no-log` options are given. If a playback is resumed from a gap log file using the `--resume=<log_file>` option, then the gap log is updated in place.

`rsn_gaps` is augmented by `status_check.py` and `data_check.py`, which are discussed indivually below, but are shown in the workflow section that follows.

### Typical Workflow
1. Determine reference designators and time periods to check for gaps
2. Run `rsn_gaps.py` with:
   1. Reference designators defined by:
      * `-r <rd1> <rd2> <rd3>`, OR
      * `--refdes=<rd1>,<rd2>,<rd3>`
   2. Gap time windows to check defined by:
      * `-t <YYYY-MM> <YYYY-MM>`, OR
      * `--times=<YYYY-MM>,<YYYY-MM>`
   3. Server to play back to:
      * `-s <prod|dev01|dev03>`, OR
      * `--server=<prod|dev01|dev03>
      * Usually, setting the server to `dev03` is recommended to test and verify playback prior to release to production
   4. Optional variables (see options section below). Altneratively, you can use a playback options file to set the reference designator list and times list (see options below).
3. This will start a gap check (on production data) to identify all gaps greater than 24 hours in the one month periods following the time window dates you defined in step 2-ii above for each reference designator defined in step 2-i above.
4. When the gap check finishes, you will shown the gap list JSON output and prompted as to whether to continue with play back to the specified server.
5. If you choose to start playback, the job numbers assigned to each playback request (one for each gap) will be saved to the gap log file and the program will exit.
6. You can check the status of these jobs by running the `status_check.py` tool (see examples below)
7. When all playback have completed, you can verify playback by using the `data_check.py` verification plot tool (see examplse below).
8. Once test playback have been verified, run `rsn_gaps.py` again with the `--resume=<gap_file>` and `--server=prod` options to complete the playbacks on the production OOINet server.
   1. Again, the log file will be updated with the new production playback job IDs.
9. You can check statuses again as in step 6 and verify playback as in step 7 (see examples below)
10. You're done!

### Example Workflow
Here, we'll check for gaps and play back data for DOSTA instruments for the time period of the month of January 2020.

First, we want to run the gap check and playback tool, playing back to `dev03`:
```bash
[user@test]: cd /path/to/rsn_tools/gap_finder/
[user@test]: python rsn_gaps.py -r RS03AXPS-PC03A-4A-DOSTAD303 -t 2020-01 --server=dev03
```
Which gives the output:
```bash
Building gaps from scratch
Instantiating instrument object for: RS03AXPS-PC03A-4A-DOSTAD303... Done
Building URL... Done
REQUEST INFO:
   Server:   prod
   URL Base: https://ooinet.oceanobservatories.org/api/m2m/12576/sensor/inv/
   Begin:    2020-01-01T00:00:00.000Z
   End:      2020-02-01T00:00:00.000Z
Requesting dissolved_oxygen data from M2M... Done
Processing data... Done

Playing back!
{
    "RS03AXPS-PC03A-4A-DOSTAD303": [
        {
            "refdes": "RS03AXPS-PC03A-4A-DOSTAD303",
            "start": "2020-01-29T00:02:31.000Z",
            "end": "2020-01-29T17:37:59.000Z",
            "job": null,
            "test": "Not Started",
            "prod": "Not Started"
        }
    ]
}
Are you sure you want to play back to dev03? [y/n]: y
RS03AXPS-PC03A-4A-DOSTAD303 {'message': 'Element created successfully.', 'id': 907, 'statusCode': 'CREATED'}
Writing logfile: ./rsn_gaplist_2020-03-03T19_52Z.log
```
The resultant log file would look like this:
```
{
  "gap_list": {
    "RS03AXPS-PC03A-4A-DOSTAD303": [
      {
        "refdes": "RS03AXPS-PC03A-4A-DOSTAD303",
        "start": "2020-01-29T00:02:31.000Z",
        "end": "2020-01-29T17:37:59.000Z",
        "job": 907,
        "test": "PENDING",
        "prod": "Not Started"
      }
    ]
  },
  "run_info": {
    "run_date": "2020-03-03T19:52:04.178219",
    "command": "rsn_gaps.py -r RS03AXPS-PC03A-4A-DOSTAD303 -t 2020-01 -s dev03",
    "refdes": [
      "RS03AXPS-PC03A-4A-DOSTAD303"
    ],
    "times": [
      "2020-01"
    ],
    "server": "dev03"
  }
}
```
Then, run the status check using the gap log file generated by `rsn_gaps.py` to occasionally check the status of your playback job(s):
```bash
[user@test]: python status_check.py ./rsn_gaplist_2020-03-03T19_52Z.log
```
If the job hasn't started or no files were found to play back, you'll see:
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {}
```
If the job has started, you'll see:
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {'PENDING': 1}
```
meaning one file was found and is pending playback. Then
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {'QUEUED': 1}
```
meaning that file has been queued and is awaiting playback. Sometimes with a larger number of files you'll see a `SENT` field, which means those files have been sent from the queue to the playback engine. Finally, you'll see:
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {'COMPLETE': 1}
```
indicating that all of the files found for playback have been played back. If you have multiple gaps you're playing back, wait for all of them to reach a compelted state. Sometimes you'll get individual file warnings, which need to be investigated prior to moving on to playback on production. In this example, that isn't an issue, so we'll carry on as expected.

Once all of the test playback jobs have completed, it's time to verify the data using the `data_check.py` tool. This tool reads the gap list and plots a test variable for the given gap time period so you can visually inspect the played back data. Here's an example:
```bash
[user@test]: python data_check.py rsn_gaplist_2020-03-03T19_52Z.log
```
Visually inspect the plotted data for unexpected gaps and correct data ranges and then close the plot to continue to the next plot or quit if just a single plot.

Now, we can resume the playback from the gap file using the `rsn_gaps.py` tool:
```bash
python rsn_gaps.py --resume=rsn_gaplist_2020-03-03T19_52Z.log --server=prod
```
When you choose production as your playback server, you'll be prompted if you really want to do that with some snarky dialogs. You must type out the full word `yes` and press enter to continue. The gap information will be displayed and you'll be asked one more time if you'd like to continue. Here you can just type `y` and hit enter. Again, playback job information will be printed and the log file will be updated with new job IDs. Here's the output for our example:
```
== WARNING ================================================
 Hey buddy...
 You set playback server to PRODUCTION...

 Are you sure you want to do that? [yes/n]: yes

Your call... Carrying on (but not keeping calm).

Loading gaps from file
Playing back!
{
    "RS03AXPS-PC03A-4A-DOSTAD303": [
        {
            "refdes": "RS03AXPS-PC03A-4A-DOSTAD303",
            "start": "2020-01-29T00:02:31.000Z",
            "end": "2020-01-29T17:37:59.000Z",
            "job": 907,
            "test": "PENDING",
            "prod": "Not Started"
        }
    ]
}
Are you sure you want to play back to prod? [y/n]: y
RS03AXPS-PC03A-4A-DOSTAD303 {'statusCode': 'CREATED', 'message': 'Element created successfully.', 'id': 18215}
Updating logfile: rsn_gaplist_2020-03-03T19_52Z.log
```
And now the log file looks like this:
```
{
  "gap_list": {
    "RS03AXPS-PC03A-4A-DOSTAD303": [
      {
        "refdes": "RS03AXPS-PC03A-4A-DOSTAD303",
        "start": "2020-01-29T00:02:31.000Z",
        "end": "2020-01-29T17:37:59.000Z",
        "job": 18215,
        "test": "COMPLETE",
        "prod": "PENDING"
      }
    ]
  },
  "run_info": {
    "run_date": "2020-03-04T23:11:23.554316",
    "command": "rsn_gaps.py --resume=rsn_gaplist_2020-03-03T19_52Z.log --server=prod",
    "refdes": [],
    "times": [],
    "server": "prod"
  }
}
```
You can see that the job number has been updated to the new job on production and that hte test and prod status has been changed to `COMPLETE` and `PENDING` respectively. I need to add a `--finalize` option to update final statuses, but I've not figured out the best way to implement this.

As before, you can check that status using the `status_check.py` tool, which will automatically read the server field from the gap file and check the correct server for playback status. When all of the playbacks have finished, you can again run the `data_check.py` tool (which will also use the correct server from the gap file) to verify that all playbacks have completed successfully. Now, just update any Redmine or Purplemine tickets related to the playback and go on your merry way.

### Playback Options File
Reference designators and gap window times can be defined in bulk by using a playback options configuration file. These files have the following format:
```
[refdes]
CE04OSBP-LJ01C-05-ADCPSI103
RS01SUM2-MJ01B-12-ADCPSK101
CE02SHBP-LJ01D-05-ADCPTB104
RS01SBPS-PC01A-05-ADCPTD102
RS03AXPS-PC03A-05-ADCPTD302

[times]
2016-10
2019-11
2019-12
2020-01
```
You can save the file in any fromat, but I recommend something like `gap_options_<date>.cfg`. More information can be found by running `python rsn_gaps.py --file=help`.

### Other Options

#### All Reference Designators (`-a`, `--all`):
Use of the `-a` or `--all` flag will query `rsn-tools.core.streams.rdList` to return a full list of reference designators currently supported by the RSN-tools package. Doing so will allow gap detection and playback for all reference designatos. When using this option, the `-r` and `--refdes=` options are ignored if provided.
Note: Must be the first option in the options list!

#### Check Gaps Only (`-c`, `--check-only`):
Use of the `-c` or `--check-only` options will prevent playback after gap detection. Hence, the tool will only check for gaps and return a gap log file. Use this option with the `--file`, `-r`, and `-t` options; `-s` will be ignored.

#### Read Reference Designators and Times from FIle (`-f`, `--file`):
Certain gap detection and playback options can be defined in bulk in an options file and passed to `rsn_gaps.py` using the `-f` or `--file` flag. Here are a few examples of the use case:
* `python rsn_gaps.py -f sf01a_2018_options.cfg`
* `python rsn_gaps.py --file=sf01a_2018_options.cfg`
* `python rsn_gaps.py -f help` <-- displays help for the options file
* `python rsn_gaps.py --file=help` <-- displays help for the options file
See the Playback Options File section above for more info and file formatting requirements.
Note: Must be the first option in the options list!

#### Force Playback (`--force`):
Use of the `--force` option when `--preview` and `--check-only` are not used will set the `checkExistingFiles` parameter in the playback request to `false`, so that a playback can be repeated without files getting ignored. This can be helpful if a playback was canceled or if some other error occured and the playback needed to be re-done. Use this sparingly, as it's not ideal to have multiple copies of the same data in UFRAME.

#### Get Help (`-h`, `--help`):
Use this as the first option and with no other options (other options will be ignored) to display a help message with all of the available options.

#### Don't Update/Create a Log File (`--no-log`):
If you're doing a test playback or a one-off playback unrelated to production and don't want a log file to be written or updated for whatever reason, you can use the `--no-log` option to bypass writing/updating of the gap log file.

#### Set the Log Path (`--log-path`):
By default, gap log files are written in the present working directory, or the directory that `rsn_gaps.py` is run (usually `.../rsn_tools/gap_finder/`), however, a different path can be set by using the `--log-path` option. When using the option, only specify the log path - do NOT include a filename. Filename's are automatically generated by the program. Here's an example use case:
```bash
python rsn_gaps.py -r CE04OSBP-LJ01C-05-ADCPSI103 -t 2020-01 --log-path=/home/username/gap_log_files/
```
In this example the gap log file for ADCPSI103 during 2020-01, a log file would be written to `/home/username/gap_log_files/rsn_gaplist_2020-03-03T19_52Z.log`.


#### Playback Preview (`--preview`):
The `--preview` option prevents playback and only displays the playback request for inspection. It will also bypass logging.

#### Set Reference Designators (`-r`, `--refdes`):
This flag sets reference designators to be checked for gaps and played back. Here are some usage examples:
* `pyhton rsn_gaps.py -r CE04OSBP-LJ01C-05-ADCPSI103 RS01SUM2-MJ01B-12-ADCPSK101 -t 2020-01`
* `pyhton rsn_gaps.py --refdes=CE04OSBP-LJ01C-05-ADCPSI103,RS01SUM2-MJ01B-12-ADCPSK101 -t 2020-01`

#### Resome from Gap File (`--resume`):
The `--resume` flag allows you to pickup where you left of. If you ran the gap check with the `--check-only` flag, you can start a playback on those gaps by using the `--resume` option. Likewise, if you've played back to a test server and are ready to play back to production, you can use the resume option as well. Here are some examples:
* `python rsn_gaps.py --resume=rsn_gaplist_2020-03-03T19_52Z.log --server=dev03` will take a gap only log and start a playback on `dev03`
* `python rsn_gaps.py --resume=rsn_gaplist_2020-03-03T19_52Z.log --server=prod` will take a gap file and start playback on production
* `python rsn_gaps.py --resume=rsn_gaplist_2020-03-03T19_52Z.log --server=dev03 --force` is an example of how to resume a failed playback

#### Set Playback Server (`-s`, `--server`):
You can tell `rsn_gaps.py` to playback to a specific server by using the `-s <server>` or `--server=<server>` option. Replace `<server>` with either `dev03`, `dev01`, or `prod`. If the server option is not given, the program will default to `dev03`. This option is ignored if `--check-only` is used.

#### Set Gap Checking Time Windows:
Gap check time windows are in the format of "YYYY-MM" - a four digit year followed by a dash and a two digit (zero padded) month. These times imply that gap checks will start on the first of a month, and the program will automatically ensure that they end on the first day of the following month. So, for example, using `-t 2020-01` will check for gaps between 2020-01-01T00:00:00.000Z and 2020-02-01T00:00:00.000Z. Here are some use examples:
* `python rsn_gaps.py -r CE04OSBP-LJ01C-05-ADCPSI103 -t 2019-12 2020-01 2020-02`
* `python rsn_gaps.py -r CE04OSBP-LJ01C-05-ADCPSI103 --times=2019-12,2020-01,2020-02`


## status_check.py - Main Program

### Description
`status_check.py` reads in a gap log file and checks Ingest Engine for the status of each jobID. The gap log file contains information on the last server used for playback, and this is used by `status_check.py` to determine which server to check for playback statuses.

### Typical Use Case
The only use case is to use `status_check.py` to check the status of playbacks started by `rsn_gaps.py`. Here's how:
```bash
[user@test]: cd /path/to/rsn_tools/gap_finder/
[user@test]: python status_check.py rsn_gaplist_2020-03-03T19_52Z.log
```
The following are typical responses from the status checkt tool.

If the job hasn't started or no files were found to play back, you'll see:
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {}
```
If the job has started, you'll see:
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {'PENDING': 1}
```
meaning one file was found and is pending playback. Then
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {'QUEUED': 1}
```
meaning that file has been queued and is awaiting playback. Sometimes with a larger number of files you'll see a `SENT` field, which means those files have been sent from the queue to the playback engine. Finally, you'll see:
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {'COMPLETE': 1}
```
There can be any combination of these as well, for example:
```
RS03AXPS-PC03A-4A-DOSTAD303 (dev03):
   907 {'QUEUED': 5, 'SENT': 12', COMPLETE': 9, 'PENDING': 10}
```

### Other Options
At present, there are no additional options for the status check tool.

### The Future and Beyond
In the future, this will be modified to check for a fully completed status. If found, the gap log file will updated to say that the playback is complete.