# Release Notes

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
