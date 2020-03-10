# Release Notes

## Version 4.0.0
* Directory and file restructure and addition of setup.py to be pip installable.

## Version 3.4.4
* Fixed a bug in `rsn_gaps.py` where the file help fails to quit.

## Version 3.4.3
* Added `--no-log` option to `rsn_gaps` to avoid logging for one-time playbacks, etc.

## Version 3.4.2
* Added data check program to generate verification plots from gap log file.

## Version 3.4.1
* Added status check program to check status based on gap log file.

## Version 3.4.0
* Modified filemask creation to use raw CTD files for DOSTA playback instead of port agent datalogs.

## Version 3.3.3
* Added playback request preview option to CLI.
* Fixed a bug that prevented update of job numbers when resuming playback from file on a different server.

## Version 3.3.2
* Added reading of gaplist from a file to `playback.py`.
* Minor improvements to `rsn_gaps.py`.

## Version 3.3.1
* Modified `core.playback.gapListObj.dump()` routine to return JSON element when given `filename='JSON'` as an argument.
* Added log file path flag to `rsn_gaps.py`.
* Added gap logging output.

## Version 3.3.0
* Added functionality to detect gaps in `rsn_gaps.py` which is built off the rest of the package.
* Multiple bug fixes.

## Version 3.2.4
* Bug fixes and a job list print function.

## Version 3.2.3
* Modified `core.engine.InstDataObj.get_metadata_times()` to allow partial searches on stream names for `metadata/times` return.

## Version 3.2.2
* Added bulk playback routine to `core.playback` module.

## Version 3.2.1
* Added gap list data structure object and data gap object and associated functions and helpers.

## Version 3.1.1
* Removed requirement to specify file dates by adding file date generation from gap date specification.

## Version 3.1.0
* Restructured `core.ooicrds` (and correspoinding example) to include username.
* Added `core.m2mlib.getUser()` to retrieve username from `core.ooicreds`.
* Modified `core.m2mlib.MachineToMachine.__init__()` to extract username from `core.ooicreds`
* Updated `core.playback` to reflect above changes.

## Version 3.0.0
* Integrated Dan Mergens' playback tool as `core.m2mlib` and `core.playback`.

## Version 2.3.5
* #246 - Added an 'all' option to `core.engine.get_metadata_times()` to show timing metadata for all streams associated with a reference designator.

## Version 2.3.4
* Added parameter print function to `InstDataObj` class.
* Changed default parameter for SPKIRA sensors in `core.streams.rdList`

## Version 2.3.3
* Changed OPTAA default variable from `pressure_counts` to `external_temp_raw`.
* Added option to display a blank plot if no data returned in `core.engine.go()`.

## Version 2.3.2
* #231 - Added missing instruments to `core.streams.rdList`.

## Version 2.3.1
* Extended timeout from 20 to 60 seconds in `core.engine.get_data()`.
* Added exception handling for `requests.exceptions.Timeout`.

## Version 2.3.0
* #219 - Added `core.engine.get_metadata_times()` function for requesting start/end times for a stream.

## Version 2.2.0
* Added `self.stream` to `core.engine.InstDataObj`.
* Added `self.fullrd` to `core.engine.InstDataObj`.
* Cleaned up `InstdataObj` init code.
* Added endpoint inclusion to `core.engine.getBaseURL()`

## Version 2.1.0
* Added a ref-des search by instrument name as `core.engine.RDsearchByInst()`.

## Version 2.0.1
* Removed debugging code and improved log messages.

## Version 2.0.0
* Modified `playback_check` to be a callable package. Redefined all imports to use package structure. Renamed `playback_check.py` to `engine.py`.

## Version 1.3.0
* Added `self.quickPlot()` function to `playback_check.py` to quickly plot data if you're not using `self.go()`.

## Version 1.2.2
* Fixed \t sneaky character in `pdName` field for BOTPTs in `streams.py`.

## Version 1.2.1
* Changed x-axis limits to use the user-specified start/end times instead of the min/max of returned data to better show data return versus time bracket.

## Version 1.2.0
* #203 - Added DOSTA instruments to `streams.py` as they were previously missing.

## Version 1.1.1
* Increased M2M request timeout from 10 seconds to 20 seconds to prevent frequent timeouts.

## Version 1.1.0
* #201 - Added DOSTA instruments to `streams.py` as they were previously missing.

## Version 1.0.0
* #199 - Initial creation of `playback_check`, supporting modules, documentation, and examples.
