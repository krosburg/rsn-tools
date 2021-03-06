# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:12:23 2019

@author: K.C. Rosburg, APL/UW
"""

from datetime import datetime, timedelta
from rsn_tools.core.streams import rdList
from rsn_tools.core.ooicreds import PROD_CREDENTIALS, DEV01_CREDENTIALS, DEV03_CREDENTIALS
from requests.exceptions import Timeout
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getCreds(srv):
    """ Get credentials based on server specification """
    if srv == "prod":
        return PROD_CREDENTIALS
    elif srv == "dev01" or srv == "pre-prod":
        return DEV01_CREDENTIALS
    elif srv == "dev03" or srv == "test":
        return DEV03_CREDENTIALS
    else:
        raise Exception("Credentials not configured for " + srv + ". Abort!")
        
def getBaseURL(srv, use_endpoint=True):
    """ Get base URL based on server specification. IF use_endpoint is True or
        not specified the sensor inventory endpoint will be added to the URL.
        If use_endpoint is False, just the main domain URL will be used."""
    ENDPOINT = 'api/m2m/12576/sensor/inv/'
    # Define main domain URL based on server designation (or quit w/ error)
    if srv == "prod":
        url = 'https://ooinet.oceanobservatories.org/'
    elif srv == "dev01" or srv == "pre-prod":
        url = 'https://ooinet-dev-01.oceanobservatories.org/'
    elif srv == "dev03" or srv == "test":
        url = 'https://ooinet-dev-03.oceanobservatories.org/'
    else:
        raise Exception("BASE_URL not configured for " + srv + ". Abort!")
    # Add enpoint if requested
    if use_endpoint:
        return url + ENDPOINT
    return url


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
        self.fullrd = rdList[refdes]['fullrd']
        self.ref_des = refdes
        self.pdnums = rdList[refdes]['testPD']
        self.pnames = [rdList[refdes]['pdName']]
        self.method = 'streamed'
        self.stream = rdList[refdes]['stream']
        self.url_part = '/'.join([self.fullrd, 'streamed', self.stream])
        self.URL = ""
        self.t = []
        self.x = []
        self.y = []
        print(' Done')
        

    def build_url(self, beginDT, endDT, srv, DEBUG=False):
        print('Building URL...', end='')
        BASEURL = getBaseURL(srv, use_endpoint=True)
        LIMIT = 1000
        self.URL = BASEURL + self.url_part \
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
            
            
    def get_metadata_times(self, srv, stream=None):
        if not stream:
            stream = self.stream
        url = '/'.join([getBaseURL(srv), self.fullrd, 'metadata', 'times'])
        metadata = requests.get(url, auth=getCreds(srv),
                                timeout=20, verify=False)
        if metadata.status_code != 200:
            print(' FAIL')
            print('ERROR: Request failed with: %i\n' % metadata.status_code)
            return []
        if stream.lower() == 'all':
            return metadata.json()
        #return [x for x in metadata.json() if x['stream'] == stream][0]
        return [x for x in metadata.json() if stream in x['stream']]
            
            
    def get_data(self, srv):
        """ Given a request URL, returns a json element with the data from M2M """
        username, token = getCreds(srv)
        SUCCESS_CODE = 200
        print('Requesting ' + self.pnames[0] + ' data from M2M...', end='')
        try:
            raw_data = requests.get(self.URL, auth=(username, token),
                                    timeout=60, verify=False)
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
                
        except Timeout:
            print(' FAIL')
            print('ERROR: Request timed out.\n')
                
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

    
    def print(self):
        print('=== Instrument Object ====')
        print('Ref-des:  ' + self.ref_des)
        print('PD Nums:  ' + self.pdnums)
        for pname in self.pnames:
            print('PD Names: ' + pname)
        print('Method:   ' + self.method)
        print('Stream:   ' + self.stream)
        
    
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
    
    
    def go(self, beginDT, endDT, srv, fsize=(15, 4), DEBUG=False, err_plt=True):
        """ Builds URL, get data, then plots.
            Takes in ISO format begin and end times, server name
            ('prod', 'dev03', etc.) and an optional figure size as a tuple
            [e.g. (15, 4)] in inches.
        """
        self.build_url(beginDT, endDT, srv, DEBUG)
        if self.get_data(srv): 
            # Plot
            self.quickPlot(beginDT, endDT, fsize=fsize)
        else:
            if err_plt:
                fig = plt.figure(figsize=fsize)
                plt.plot()
                plt.text(0, 0, 'ERROR',
                         ha='center', va='center', size=40, color='red')
                plt.text(0, -0.02, 'No Data Returned from M2M Query',
                         ha='center', va='center', size=20, color='black')
                plt.title(self.ref_des + ' ' + self.pnames[0])
        plt.show()