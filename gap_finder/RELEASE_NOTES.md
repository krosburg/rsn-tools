# Release Notes

## Version 1.3.0
* #220 - `gap_cli.py` now uses M2M metadata/times bounds to a) skip gap logging if the given time range is outside of the M2M data range or b) prevent logging of false start/end gaps if a given time range starts/ends outside of the M2M data range.

## Version 1.2.0
* #217 - Created a tool to generate bulk scripts for `gap_cli.py` use.

## Version 1.1.3
* #216 - Handle edge case where `gap_cli.py` cannot handle an empty data return.

## Version 1.1.2
* #215 - Stopped `gap_cli.py` from creating gap logs if no gap exists.

## Version 1.1.1
* Removed debugging code in `gap_cli.py` and improved log output.

## Version 1.1.0
* #213 - Added `gap_cli.py` to textually log data gaps in M2M by refdes using a command line interface.

## Version 1.0.0
* #212, #214 - Initial creation of `gap_finder` with `plot_gaps.py` to check for gaps visually.
