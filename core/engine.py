# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:12:23 2019

@author: K.C. Rosburg, APL/UW
"""

from datetime import datetime, timedelta
from core.streams import rdList
from core.ooicreds import PROD_CREDENTIALS, DEV01_CREDENTIALS, DEV03_CREDENTIALS
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getCreds(srv):
    """ Get credentials based on server specification """
    if srv is "prod":
        return PROD_CREDENTIALS
        #return ('OOIAPI-25Q505KHEZGN7M', '8Y7ID166LLNXU7')
    elif srv is "dev01" or srv is "pre-prod":
        return DEV01_CREDENTIALS
    elif srv is "dev03" or srv is "test":
        #return ('OOIAPI-1ADRQA60R9CG8G', 'TEMP-TOKEN-0EMZVNOD7BK9LS')
        return DEV03_CREDENTIALS
    else:
        raise Exception("Credentials not configured for " + srv + ". Abort!")
        
def getBaseURL(srv):
    """ Get base URL based on server specification """
    if srv is "prod":
        return 'https://ooinet.oceanobservatories.org/'
    elif srv is "dev01" or srv is "pre-prod":
        return 'https://ooinet-dev-01.oceanobservatories.org/'
    elif srv is "dev03" or srv is "test":
        return 'https://ooinet-dev-03.oceanobservatories.org/'
    else:
        raise Exception("BASE_URL not configured for " + srv + ". Abort!")


def epoch_to_dt(t):
    """ Convert epoch date to date time """
    # Setup Offsets
    offset = datetime(1970, 1, 1, 0, 0, 0)-datetime(1900, 1, 1, 0, 0, 0)
    off_sec = timedelta.total_seconds(offset)

    # Convert using offsets
    t_datetime = []
    for tt in t:
        t_sec = tt - off_sec
        t_datetime.append(datetime.utcfromtimestamp(t_sec))

    return t_datetime


def RDsearchByInst(inst):
    return next( (key for key in rdList if key.endswith(inst)), None)


class InstDataObj(object):
    """ Main data object """
    def __init__(self, refdes):
        print('Instantiating instrument object for: ' + refdes + '...', end='')
        self.site = refdes.split('-')[0]
        self.node = refdes.split('-')[1]
        self.port = refdes.split('-')[2]
        self.inst = refdes.split('-')[3]
        self.inst_full = self.port + '-' + self.inst
        self.ref_des = refdes
        self.pdnums = rdList[refdes]['testPD']
        self.pnames = [rdList[refdes]['pdName']]
        self.method = 'streamed'
        self.stream = rdList[refdes]['stream']
        self.url_part = self.site + '/' + self.node + '/' + self.inst_full \
                     + '/streamed/' + rdList[refdes]['stream']
        self.URL = ""
        self.t = []
        self.x = []
        self.y = []
        print(' Done')
        

    def build_url(self, beginDT, endDT, srv, DEBUG=False):
        print('Building URL...', end='')
        ENDPOINT = 'api/m2m/12576/sensor/inv/'
        BASEURL = getBaseURL(srv)
        LIMIT = 1000
        self.URL = BASEURL + ENDPOINT + self.url_part \
            + '?limit=' + str(LIMIT) \
            + '&beginDT=' + beginDT \
            + '&endDT=' + endDT \
            + '&parameters=7,' + self.pdnums \
            + '&require_deployment=false'
        print(' Done')
        print('REQUEST INFO:')
        print('   Server:   ' + srv)
        print('   URL Base: ' + BASEURL)
        print('   Begin:    ' + beginDT)
        print('   End:      ' + endDT)
        if DEBUG:
            print(self.URL)
    

    def get_data(self, srv):
        """ Given a request URL, returns a json element with the data from M2M """
        username, token = getCreds(srv)
        SUCCESS_CODE = 200
        print('Requesting ' + self.pnames[0] + ' data from M2M...', end='')
        try:
            raw_data = requests.get(self.URL, auth=(username, token),
                                    timeout=20, verify=False)
            # Exit if bad status code
            if raw_data.status_code == 404:
                print(' FAIL')
                print('ERROR: No data found between given start and end dates.\n')
                return False
            elif raw_data.status_code != SUCCESS_CODE:
                print(' FAIL')
                print('Error: status code ', raw_data.status_code)
                print('Error: response.json(): \n', raw_data.json())
                return False
            else:
                print(' Done')
                
        except Exception as err:
            print(' FAIL')
            print('Exception: %s\n' % str(err))
            return False
            
        # Process Data into t and x NP Arrays
        print('Processing data...', end='')
        if len(self.pnames) < 2:
            data = pd.DataFrame.from_records(raw_data.json())
            self.t = mdates.date2num(epoch_to_dt(np.array(data['time'], dtype=np.float)))
            self.x = np.array(data[self.pnames[0]])
        else:
            data = raw_data.json()
            for datum in data:
                self.t.append(datum['time'])
                self.x.append(datum[self.pnames[0]])
                self.y.append(datum[self.pnames[1]])
            self.t = np.array(self.t, dtype=np.float)
            self.t = epoch_to_dt(self.t)
            self.t = mdates.date2num(self.t)
            self.x = np.array(self.x, dtype=np.float)
            self.y = np.array(self.y, dtype=np.float)
        print(' Done\n')
        return True
        
    
    def quickPlot(self, beginDT, endDT, fsize=(15, 4)):
        fig = plt.figure(figsize=fsize)
        plt.plot(self.t, self.x, '-o')
        ax1 = plt.gca()
        #plt.xlim([np.nanmin(self.t), np.nanmax(self.t)])
        plt.xlim([datetime.strptime(beginDT, '%Y-%m-%dT%H:%M:%S.%fZ'),
                  datetime.strptime(endDT, '%Y-%m-%dT%H:%M:%S.%fZ')])
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M\n%m/%d/%y'))
        plt.title(self.ref_des + ' ' + self.pnames[0])
        plt.grid()
    
    
    def go(self, beginDT, endDT, srv, fsize=(15, 4), DEBUG=False):
        """ Builds URL, get data, then plots.
            Takes in ISO format begin and end times, server name
            ('prod', 'dev03', etc.) and an optional figure size as a tuple
            [e.g. (15, 4)] in inches.
        """
        self.build_url(beginDT, endDT, srv, DEBUG)
        if self.get_data(srv): 
            # Plot
            self.quickPlot(beginDT, endDT, fsize=fsize)