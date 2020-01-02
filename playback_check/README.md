# playback_check
## Summary
This module is used to check the availabilty of data on a specified OOINet server during a specified time/date interval using the M2M interface.

The code will plot data found in the interval or return an error if a 404 error (no data) is returned.

## Requried Files
### streams.py
This file contains a list of all refernce designators for valid insturments and includes their science stream information as well as a chosen test parameter to be used for data checks. Update this as new instruments come online or when preload is modified for an existing instrument.

### playback_check.py
This is the heavy lifter, containing all of the functions and classes required to do an easy playback check. Dont mess with this file.

### ooicreds.py
This file contains your user credentials for the various OOINet/M2M servers that allow playback_check to do its job. This file is ommited from Github by `.gitignore` as a saftey protocol so credentials aren't made public.

You can copy the pre-existing `ooicreds_template.py` and modifiy it on your local copy to include your credentials so the software will work.

### check_example.py
Provides an example of a single instrument data check and serves as a reference for which modules need to be imported and the syntax on how to use the module.

## Basic use
1. Import the `InstDataObj` class from the `playback_check` module
1. Set the `SERVER` variable to `'prod'`, `'dev01'`, or `'dev03'` based on the server you would like to check
1. Set the `t_start` and `t_end` variables to an ISO 8601 time format. (e.g. `t_end = '2019-12-30T14:51:32.000Z'`)
1. Use a reference designator to instantiate an instrument object (e.g. `inst = InstDataObj('CE04OSPS-PC01B-4D-PCO2WA105'`)
1. Call the `go(start, end, server)` function to run and plot a data check (e.g. `inst.go(t_start, t_end, 'dev03')`)

Putting it all together, a basic data check would look like:
```python
    from playback_check import InstDataObj
    
    # Variables
    refdes  = 'CE04OSPS-PC01B-4D-PCO2WA105'
    server  = 'prod'
    t_start = '2017-08-02T00:00:00.000Z'
    t_end   = '2018-07-17T00:00:00.000Z'
    
    # Instiantiate and do check
    inst = InstDataObj('CE04OSPS-PC01B-4D-PCO2WA105')
    inst.go(t_start, t_end, srv=server, fsize=(9,3), DEBUG=False)
