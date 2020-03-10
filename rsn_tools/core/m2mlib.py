# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:20:42 2020
Adapted from Dan Mergens' cabled playback tool
    (github.com/oceanobservatories/ooi-tools/blob/master/playback)
@author: K.C. Rosburg, UW/APL
"""
# == IMPORTS ================================================================ #
import sys, requests, json
#sys.path.append("C:\\Users\\Kellen\\Code\\rsn-tools")
import rsn_tools.core.ooicreds


# == HELPER FUNCTIONS ======================================================= #
def getCreds(srv):
    """ Get credentials based on server specification """
    if srv == "prod":
        return core.ooicreds.PROD_CREDENTIALS
    elif srv == "dev01" or srv == "pre-prod":
        return core.ooicreds.DEV01_CREDENTIALS
    elif srv == "dev03" or srv == "test":
        return core.ooicreds.DEV03_CREDENTIALS
    else:
        raise Exception("Credentials not configured for " + srv + ". Abort!")
        

def setBaseURL(srv):
    if srv == "prod":
        return 'https://ooinet.oceanobservatories.org'
    elif srv == "dev01" or srv == "pre-prod":
        return 'https://ooinet-dev-01.oceanobservatories.org'
    elif srv == "dev03" or srv == "test":
        return 'https://ooinet-dev-03.oceanobservatories.org'
    else:
        raise Exception("BASEURL not configured for " + srv + ". Abort!")


def getUser(srv):
    if core.ooicreds.OOI_USERNAME is 'username':
        raise Exception("No username defined in OOICREDS. Abort!")
    else:
        return core.ooicreds.OOI_USERNAME
        

# == CLASS DEFINITIONS ====================================================== #
class MachineToMachine(object):
    def __init__(self, srv):
        self.base_url = setBaseURL(srv)
        self.api_user, self.api_key = getCreds(srv)
        self.username = getUser(srv)
        self.auth = (self.api_user, self.api_key)
        self.inv_url = self.base_url + '/api/m2m/12576/sensor/inv'
        self.ingest_url = self.base_url + '/api/m2m/12589/ingestrequest'

    def get(self, url, params=None):  # TODO remove
        response = requests.get(url, auth=self.auth, params=params)
        if response.status_code != requests.codes.ok:
            print('request failed (%s) for %s - %s' % (response.reason, url, params))
            return None
        return response.json()

    def toc(self):
        """table of contents"""
        url = '/'.join((self.inv_url, 'toc'))
        return requests.get(url).json()

    def node_inventory(self, subsite, node):
        """returns sensors on the specified node"""
        url = '/'.join((self.inv_url, subsite, node))
        return ['-'.join((subsite, node, sensor)) for sensor in self.get(url)]

    def streams(self):
        """returns list of all streams"""
        toc = self.toc()
        stream_map = {}
        toc = toc['instruments']
        for row in toc:
            rd = row['reference_designator']
            for each in row['streams']:
                stream_map.setdefault(rd, {}).setdefault(each['method'], set()).add(each['stream'])
        return stream_map
    
    def instruments(self):
        nodes = []
        for subsite in self.get(self.inv_url):
            for node in self.get('/'.join((self.inv_url, subsite))):
                nodes.extend(self.node_inventory(subsite, node))
        return nodes
    
    def inv_request(self, refdes, method=None, stream=None, payload=None):
        subsite, node, inst = refdes.split('-', 2)
        url = '/'.join((self.inv_url, subsite, node, inst))
        if method:
            url = '/'.join((url, method))
            if stream:
                url = '/'.join((url, stream))
        return self.get(url, params=payload)
    
    def playback(self, payload):
        """create a request for playback ingest"""
        return requests.post(self.ingest_url, auth=(self.api_user, self.api_key), json=payload)
    
    def ingest_status(self, request_id):
        """get the current status of an ingest request"""
        response = requests.get('/'.join((self.ingest_url, str(request_id))), auth=self.auth)
        return response
        # if response.status_code == 200:
        #     return response.json()['status']
        # else:
        #     print('invalid ingest request: %d' % request_id)
        #     return None
        
    def ingest_jobs(self, request_id):
        """get the status of all jobs created by an ingest request"""
        payload = { 'ingestRequestId': request_id }
        response = requests.get('/'.join((self.ingest_url, 'jobs')), auth=self.auth, params=payload)
        return response

    def ingest_job_counts(self, request_id):
        """get overall status on files processed by an ingest request"""
        payload = { 'ingestRequestId': request_id, 'groupBy': 'status' }
        response = requests.get('/'.join((self.ingest_url, 'jobcounts')), auth=self.auth, params=payload)
        return response

    def purge(self, refdes):
        """purge all data for a particular reference designator""" # TODO add stream option
        print('Purging %s on %s' % (refdes, self.base_url))
        on_production = False
        if 'ooinet.oceanobservatories.org' in self.base_url:
            on_production = True
        subsite, node, sensor = refdes.split('-', 2)
        payload = {
            'username': self.username,
            'subsite': subsite,
            'node': node,
            'sensor': sensor
        }
        url = '/'.join((self.ingest_url, 'purgerecords'))
        if on_production:
            print('Cowardly refusing to purge data on production. Use the following information to purge:')
            print('curl --request PUT %s \\' % url)
            print('--data \'%s\'' % json.dumps(payload))
            return None
        response = requests.put(url, auth=self.auth, json=payload)
        return response

    def metadata_times(self, refdes):
        """fetch the stream metadata for an instrument"""
        subsite, node, inst = refdes.split('-', 2)
        return self.get('/'.join((self.inv_url, subsite, node, inst, 'metadata/times')))
    
    def availability(self, refdes):
        return self.get('/'.join((self.base_url, 'api/data_availability', refdes)))
    
    def context(self):

        return '%s %s' % (self.base_url, self.username)