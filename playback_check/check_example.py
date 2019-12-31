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
"""


from playback_check import InstDataObj

# USER VARIABLES
SERVER = 'prod'
t_start = '2018-08-02T00:00:00.000Z'
t_end = '2019-07-17T00:00:00.000Z'

#rd_prefix = 'CE02SHBP-LJ01D-'
#instList = ['05-ADCPTB104', '06-CTDBPN106', '06-DOSTAD106',
#            '07-VEL3DC108', '08-OPTAAD106', '09-PCO2WB103',
#            '10-PHSEND103', '11-HYDBBA106']

instList = ['CE02SHBP-LJ01D-06-DOSTAD106',
            'CE04OSBP-LJ01C-06-DOSTAD108',
            'CE04OSPS-PC01B-4A-DOSTAD109',
            'RS01SBPS-PC01A-4A-DOSTAD103',
            'RS01SLBS-LJ01A-12-DOSTAD101',
            'RS03AXBS-LJ03A-12-DOSTAD301',
            'RS03AXPS-PC03A-4A-DOSTAD303']

for i in instList:
    # Instantiate Instrument Object
    #inst = InstDataObj(rd_prefix + i)
    inst = InstDataObj(i)
    
    # Run Data Check & Plot
    inst.go(t_start, t_end, SERVER)