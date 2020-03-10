# -*- coding: utf-8 -*-
"""
To use the data checker, set the variables:
    SERVER  - 'prod', 'dev01', 'dev03'
    t_start - Start time for the query in ISO 8601 format.
    t_end   - End time for the query in ISO 8601 format.
    
Note: ISO 8601 format is YYYY-mm-ddTHH:MM:SS.FFFZ
      (e.g. 1988-10-29T16:35:00.000Z)
      
    Once the above three variables are set, instantiate an instrument object:
        inst = InstDataObj('<ref-des>')
    and then call the go() function:
        inst.go(t_start, t_end, SERVER)
    if all goes well, a plot will magically appear.
    
Optional Variables:
    fsize=(x, y) - specifies figure size in inches (e.g. fsize=(6, 4)). Default
                   is fsize=(15,4).
    DEBUG - boolean. Specifies whther to print debug messages. Default is false.
    
Credentials file:
    The playback_check module requires an additional credentials file (igorned 
    by Git) that includes credentials for all of the servers you plan to use.
    The file should be called ooicreds.py. ooicreds_template.py is provided as
    template for this file. Rename it ooicreds.py and include your credentials.
    
IMPORTANT NOTE: MUST BE RUN FROM BASE DIRECTORY!
"""

#foobar = __import__("core.engine")
from core.engine import InstDataObj
import json
#from foobar import InstDataObj

# USER VARIABLES
SERVER = 'prod'
#SERVER = 'dev01'
SERVER = 'dev03'
t_start = '2020-03-06T20:00:00.000Z'
t_end = '2020-03-06T23:59:59.999Z'
#t_start = '2015-11-05T00:00:00.000Z'
#t_end = '2016-02-15T00:00:00.000Z'

# =============================================================================
# inst = InstDataObj('RS01SBPS-SF01A-3B-OPTAAD101')
# inst.go(t_start, t_end, SERVER)
# =============================================================================

# Set Reference Designator List
from core.streams import rdList
rds = []

NODE = 'PCO2WA105'
NODE = NODE.upper()
for rd in rdList:
    if NODE in rd:
        rds.append(rd)

for rd in rds:
    # Instantiate Instrument Object
    inst = InstDataObj(rd)
      
    # Run Data Check & Plot
    inst.go(t_start, t_end, SERVER, DEBUG=True)
    
    #print(json.dumps(inst.get_metadata_times(SERVER, stream='all'), indent=2))
 
# =============================================================================

#import core
#core.playback.view_status([882], SERVER)