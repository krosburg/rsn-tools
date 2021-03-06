# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:37:14 2020
Adapted from Dan Mergens' cabled playback tool
    (github.com/oceanobservatories/ooi-tools/blob/master/playback)
@author: K.C. Rosburg, UW/APL
"""
# == IMPORRTS ===== #
import json
from datetime import datetime, timedelta
from rsn_tools.core.m2mlib import MachineToMachine


# == PLAYBACK FORMATS, DRIVERS,  ======================================================= #
# MAP the CABLED PLAYBACK FORMATS and DRIVERS
# only need to enumerate playback formats that are not DATALOG (default) 
# ZPLSC - should be used for all ZPLSC files
# DATALOG - "should" be format for all non-ZPLSC files since 2016
# CHUNKY - pre-2016 format for files with binary data
# ASCII - pre-2016 for files containing ASCII characters

playback_formats = {
    'BOTPT': 'CHUNKY',
    'D1000': 'CHUNKY',
    'ZPLSC': 'ZPLSC',
}

# Instrument Driver/Parser Dictionary
parser_drivers = {
    'ADCPS': 'mi.instrument.teledyne.workhorse.adcp.driver',
    'ADCPT': 'mi.instrument.teledyne.workhorse.adcp.driver',
    'BOTPT': 'mi.instrument.noaa.botpt.ooicore.driver',
    'CTDBP': 'mi.instrument.seabird.sbe16plus_v2.ctdbp_no.driver',
    'CTDPFA': 'mi.instrument.seabird.sbe16plus_v2.ctdpf_sbe43.driver',
    'CTDPFB': 'mi.instrument.seabird.sbe16plus_v2.ctdpf_jb.driver',
    'D1000': 'mi.instrument.mclane.ras.d1000.driver',
    'DOSTA': 'mi.instrument.seabird.sbe16plus_v2.dosta.driver',
    'FLORD': 'mi.instrument.wetlabs.fluorometer.flort_d.driver',
    'FLORT': 'mi.instrument.wetlabs.fluorometer.flort_d.driver',
    'HPIES': 'mi.instrument.uw.hpies.ooicore.driver',
    'NUTNR': 'mi.instrument.satlantic.suna_deep.ooicore.driver',
    'OPTAA': 'mi.instrument.wetlabs.ac_s.ooicore.driver',
    'PARAD': 'mi.instrument.satlantic.par_ser_600m.driver',
    'PCO2WA': 'mi.instrument.sunburst.sami2_pco2.pco2a.driver',
    'PCO2WB': 'mi.instrument.sunburst.sami2_pco2.pco2b.driver',
    'PHSEN': 'mi.instrument.sunburst.sami2_ph.ooicore.driver',
    'PREST': 'mi.instrument.seabird.sbe54tps.driver',
    'SPKIR': 'mi.instrument.satlantic.ocr_507_icsw.ooicore.driver',
    'TMPSF': 'mi.instrument.rbr.xr_420_thermistor_24.ooicore.driver',
    'TRHPH': 'mi.instrument.uw.bars.ooicore.driver',
    'VEL3DB': 'mi.instrument.nobska.mavs4.ooicore.driver',
    'VEL3DC': 'mi.instrument.nortek.vector.ooicore.driver',
    'VELPT': 'mi.instrument.nortek.aquadopp.ooicore.driver',
    'CE04OSPS-PC01B-4A-CTDPFA109': 'mi.instrument.seabird.sbe16plus_v2.ctdpf_jb.driver',
    'RS01SBPS-PC01A-4A-CTDPFA103': 'mi.instrument.seabird.sbe16plus_v2.ctdpf_jb.driver',
    'RS03AXPS-PC03A-4A-CTDPFA303': 'mi.instrument.seabird.sbe16plus_v2.ctdpf_jb.driver',
    'RS01SBPS-PC01A-06-VADCPA101MAIN': 'mi.instrument.teledyne.workhorse.vadcp.playback4',
    'RS01SBPS-PC01A-06-VADCPA101-5TH': 'mi.instrument.teledyne.workhorse.vadcp.playback5',
    'RS03AXPS-PC03A-06-VADCPA301MAIN': 'mi.instrument.teledyne.workhorse.vadcp.playback4',
    'RS03AXPS-PC03A-06-VADCPA301-5TH': 'mi.instrument.teledyne.workhorse.vadcp.playback5',
}

# Sensor Remapping for Insts with Non-Standard RefDes
remapped_sensors = {
    'D1000A301': 'RASFLA301_D1000',
    'VADCPA101': ['VADCPA101MAIN', 'VADCPA101-5TH'],
    'VADCPA301': ['VADCPA301MAIN', 'VADCPA301-5TH'],
    'DOSTAD106': 'CTDBPN106',
    'DOSTAD108': 'CTDBPO108',
    'DOSTAD103': 'CTDPFA103',
    'DOSTAD109': 'CTDPFA109',
    'DOSTAD303': 'CTDPFA303',
    'DOSTAD101': 'CTDPFB101',
    'DOSTAD301': 'CTDPFB301',
}

# Define Filemask paths
# 1. Pior to 2017-08-10, files are stored in the top level directory
# 2. At this time, DOSTA can only be replayed using PA datalogs
# 3. Currently testing playback of DOSTA from CTD raw datalogs.
filemask_glob_old = '/rsn_cabled/rsn_data/DVT_Data/{node}/{sensor}*.dat'
filemask_glob_new = '/rsn_cabled/rsn_data/DVT_Data/{node}/{sensor}/*/*/{sensor}*_UTC.dat'
#filemask_glob_dosta = '/san_data/ARCHIVE/{refdes}/*/*/{refdes}.datalog.*'

# Map Science Stream Name To Instrument
science_streams = {
    'ADCPS': 'adcp_velocity_beam',
    'ADCPT': 'adcp_velocity_beam',
    'BOTPT': 'botpt_nano_sample',
    'CTDBP': 'ctdbp_no_sample',
    'CTDPFA': 'ctdpf_sbe43_sample',
    'DOSTA': 'do_stable_sample',
    'CE04OSPS-PC01B-4A-CTDPFA109': 'ctdpf_optode_sample',
    'RS01SBPS-PC01A-4A-CTDPFA103': 'ctdpf_optode_sample',
    'RS03AXPS-PC03A-4A-CTDPFA303': 'ctdpf_optode_sample',
    'CTDPFB': 'ctdpf_optode_sample',
    'D1000': 'd1000_sample',
    'FLORD': 'flort_d_data_record',
    'FLORT': 'flort_d_data_record',
    'HPIES': 'horizontal_electric_field',
    'NUTNR': 'nutnr_a_sample',
    'OPTAA': 'optaa_sample',
    'PARAD': 'parad_sa_sample',
    'PCO2WA': 'pco2w_a_sami_data_record',
    'PCO2WB': 'pco2w_b_sami_data_record',
    'PHSEN': 'phsen_data_record',
    'PREST': 'prest_real_time',
    'SPKIRA': 'spkir_data_record',
    'TMPSF': 'tmpsf_sample',
    'TRHPH': 'trhph_sample',
    'VADCP': 'vadcp_velocity_beam',
    'VEL3D': 'vel3d_b_sample',
    'VELPT': 'velpt_velocity_data',
}



# == FUNCTION DEFINITIONS =================================================== #
def playback_format(refdes):
    """Retrieve playback format for given refdes"""
    sensor = refdes.split('-')[3]
    sensor_type = sensor[0:5]
    file_format = playback_formats.get(sensor_type, None)
    # default format is DATALOG, however earlier raw datafiles can vary based on time (TODO)
    if not file_format:
        file_format = 'DATALOG'
    return file_format


def parser_driver(refdes):
    """Retrieve parser/driver for given refdes"""
    # check for exceptional case first (uses entire refdes)
    driver = parser_drivers.get(refdes, None)
    if not driver:
        sensor = refdes.split('-')[3]
        sensor_type = sensor[0:5]
        driver = parser_drivers.get(sensor_type, None)
        if driver is None:
            sensor_type = sensor[0:6]
            driver = parser_drivers.get(sensor_type, None)
    return driver


# TODO: ADD A SWITCH FOR OLD SENSORS
def create_filemasks(refdes):
    """file globs specific to the sub-range from the most recent outage"""
    _, node, _, sensor = refdes.split('-', 3)
    filemasks = []
    if sensor in remapped_sensors.keys():
        sensor = remapped_sensors[sensor]
    if type(sensor) != list:
        sensor = [sensor]
    # print(sensor)
    for s in sensor:
        #if 'DOSTA' in s:
        #    filemasks.append(filemask_glob_dosta.format(refdes=refdes))
        #else:
        filemasks.append(filemask_glob_new.format(node=node.lower(), sensor=s))
    return filemasks


def science_stream(refdes):
    stream = science_streams.get(refdes, None)
    sensor_type = refdes.split('-')[3][0:5]
    if not stream: # try 5 sensor_type code
        stream = science_streams.get(sensor_type, None)
        if not stream: # second pass for 6 character specific streams (e.g. PCO2WA)
            sensor_type = refdes.split('-')[3][0:6]
            stream = science_streams.get(sensor_type, None)
    return stream


def cabledRequestFactory(username, refdes, filemasks, file_range=None,
                         data_range=None, force=False, priority=5, max_files=None):
    subsite, node, sensor = refdes.split('-', 2)
    request = {
        'username': username,
        'state': 'RUN',
        'type': 'PLAYBACK',  # 'RECOVERED', 'TELEMETERED', 'PLAYBACK'
        'options': {
        },
        'ingestRequestFileMasks': [],
    }
    request['priority'] = priority
    if max_files:
        request['maxNumFiles'] = max_files
    request['options']['format'] = playback_format(refdes)

    driver = parser_driver(refdes)
    if driver is None and 'VADCP' not in refdes:
        print('unable to find driver for sensor: ', refdes)
        return None

    for mask in filemasks:
        if 'VADCP' in refdes:
            if 'MAIN' in mask:
                driver = parser_driver(refdes + 'MAIN')
            elif '-5TH' in mask:
                driver = parser_driver(refdes + '-5TH')
            else:
                print('unable to find driver for sensor: ', refdes)
                return None
            
        request['ingestRequestFileMasks'].append(
        {
            'dataSource': 'streamed',
            'refDes': {
                'full': True,
                'node': node,
                'sensor': sensor,
                'subsite': subsite,
            },
            'refDesFinal': True,
            'parserDriver': driver,
            'fileMask': mask,
            'deployment': 0,  # always 0 for cabled playback
        })

    if file_range:
        request['options']['beginFileDate'] = file_range[0]
        request['options']['endFileDate'] = file_range[1]

    if data_range:
        request['options']['beginData'] = data_range[0]
        request['options']['endData'] = data_range[1]
    
    if force:
        request['options']['checkExistingFiles'] = False
    
    return request


class gapObj(object):
    def __init__(self, refdes, t_start, t_end, jobID=None):
        self.refdes= refdes
        self.start = t_start
        self.end = t_end
        self.job = jobID
        self.test = 'Not Started'
        self.prod = 'Not Started'
        
    def update(self, jobID, test_status=None, prod_status=None, force=False):
        if force or self.job is None:
            self.job = jobID
        if test_status is not None:
            self.test = test_status
        if prod_status is not None:
            self.prod = prod_status
        
    def print(self):
        print('-- %s ----------' % self.refdes)
        print('  * Start: %s' % self.start)
        print('  * End:   %s' % self.end)
        print('  * JobID: ', end='')
        if self.job is not None:
            print(self.job)
        else:
            print('')
        print('  * Test:  %s' % self.test)
        print('  * Prod:  %s' % self.prod)
        
    def dump(self):
        return {'refdes': self.refdes,
                'start': self.start,
                'end': self.end,
                'job': self.job,
                'test': self.test,
                'prod': self.prod}
        
        
class gapListObj(object):
    """Data structure (dictionary) that holds gapObjs tied to a refdes."""
    def __init__(self, server, rundate=None):
        self.data = {}
        if rundate is None:
            self.run_date = datetime.utcnow()
        else:
            self.run_date = rundate
        self.updated = datetime.utcnow()
        self.server = server
        
    def add(self, refdes, t_start, t_end, jobID=None):
        """ Adds a new gapObj to the gap list, if refdes not present, adds."""
        new_gap = gapObj(refdes, t_start, t_end, jobID)
        if refdes in self.data:
            self.data[refdes].append(new_gap)
        else:
            self.data[refdes] = [new_gap]
        self.touch()
            
    def update(self, refdes, jobID, test_status=None, prod_status=None, newID=None):
        """Update various gap job information. Uses refdes + jobID combo to
        lookup correct entry. If newID is given, the jobID will be updated."""
        if test_status is None and prod_status is None and newID is None:
            return False
        for gap in self.data[refdes]:
            if gap.job == jobID:
                if newID is None:
                    gap.update(jobID, test_status, prod_status)
                else:
                    gap.update(newID, test_status, prod_status, force=True)
                self.touch()
                return True
            
    def touch(self):
        self.updated = datetime.utcnow()
        
    def stat(self):
        print('Run Date: ' + datetime.isoformat(self.run_date)[:-3] + 'Z')
        print('Modified: ' + datetime.isoformat(self.updated)[:-3] + 'Z')
        
    def print_all(self):
        for rd in self.data:
            for gap in self.data[rd]:
                gap.print()

    def dump(self, filename=None):
        gapList = {}
        for rd in self.data:
            this_item = []
            for gap in self.data[rd]:
                this_item.append(gap.dump())
            gapList[rd] = this_item
        if filename is None:
            print(json.dumps(gapList, indent=4))
        elif filename is 'JSON':
            return gapList
        else:
            with open(filename, 'w+') as f:
                f.write(json.dumps(gapList, indent=3))
                
    def jobs(self, print=False):
        job_list = []
        for rd in self.data:
            for gap in self.data[rd]:
                if gap.job is not None:
                    job_list.append(gap.job)
                    if print:
                        print('%s, %s' % (rd, gap.job))
        return job_list

    
    def status(self):
        for rd in self.data:
            for gap in self.data[rd]:
                if gap.job is not None:
                    print('%s (%s):\n   ' % (rd, self.server), end='')
                    view_status(gap.job, self.server)
                    
    

def gaplist_from_file(filename):
    """Reads a gaplist from file. File should be in JSON format."""
    with open(filename, 'r') as fh:
        data = json.load(fh)
    gaplist = gapListObj(data['run_info']['server'],
                         datetime.strptime(data['run_info']['run_date'], '%Y-%m-%dT%H:%M:%S.%f'))
    for rd in data['gap_list']:
        for gap in data['gap_list'][rd]:
            # Add Each Entry to gaplist
            gaplist.add(gap['refdes'], gap['start'], gap['end'], gap['job'])
            # If job ID, then update test status and prod status
            if gap['job'] is not None:
                gaplist.update(gap['refdes'], gap['job'], gap['test'], gap['prod'])
    return gaplist


def server_from_file(filename):
    """Returns playback server of last run from a gap log file."""
    with open(filename, 'r') as fh:
        data = json.load(fh)
    return data['run_info']['server']
            

def get_filerange(data_range):
    """Returns a file date range from a gap date range."""
    if data_range is None:
        return None
    fmt = '%Y-%m-%d'
    # Add one day to reflect exclusive end time in playback engine
    tend = datetime.strptime(data_range[1][0:10], fmt) + timedelta(days=1)
    return (data_range[0][0:10], datetime.strftime(tend, fmt))
    

def run_playback(server, refdes, data_range=None, force=False, DEBUG=False):
    # Create M2M Object
    m2m = MachineToMachine(server)
    m2m.context()
    filemasks = create_filemasks(refdes)
    request = cabledRequestFactory(m2m.username, refdes, filemasks,
                                   file_range=get_filerange(data_range), 
                                   data_range=data_range, force=force)
    if DEBUG:
        print(json.dumps(request, indent=4))
    response = m2m.playback(request)
    return response


def preview_playback(server, refdes, data_range=None, force=False, DEBUG=False):
    # Create M2M Object
    m2m = MachineToMachine(server)
    print(m2m.context())
    filemasks = create_filemasks(refdes)
    request = cabledRequestFactory(m2m.username, refdes, filemasks,
                                   file_range=get_filerange(data_range), 
                                   data_range=data_range, force=force)
    print(json.dumps(request, indent=4) + '\n')
    
    
def bulk_playback(server, rdList, preview_only=True, force=False, DEBUG=False):
    if not preview_only and input('Are you sure you want to play back to ' + server + '? [y/n]: ').lower() != 'y':
        print('USER ABORTED PLAYBACK. EXITING.')
        return False
    for refdes in rdList.data:
        for gap in rdList.data[refdes]:
            data_gap = (gap.start, gap.end)
            # Preview Only Mode Just Prints the Requests
            if preview_only:
                preview_playback(server, refdes, data_range=data_gap, force=force, DEBUG=DEBUG)
            else:
                # Sumit the Request
                try:
                    response = run_playback(server, refdes, data_range=data_gap, force=force, DEBUG=DEBUG)
                except ValueError as Err:
                    print('ERROR: Invalid time range!')
                    continue
                if response:
                    # Display response and update job id field of each gap
                    print(refdes, response.json())
                    if 'dev' in server or 'test' in server or 'pre' in server:
                        gap.update(response.json()['id'], test_status='PENDING', force=True)
                    else:
                        gap.update(response.json()['id'], test_status='COMPLETE', prod_status='PENDING', force=True)
                else:
                    print('no response for playback request of %s' % refdes)
    
    
def view_status(job_list, server):
    m2m = MachineToMachine(server)
    if type(job_list) != list:
        job_list = [job_list]
    for job in job_list:
        counts = {}
        job_status = m2m.ingest_jobs(job).json()
        for x in job_status:
            status = x['status']
            prev_count = counts.get(status, None)
            if prev_count is None:
                counts[status] = 1
            else:
                counts[status] = prev_count + 1
            if status in [u'ERROR', u'WARNING']:
                print(x['status'], x['filePath'])
        print(job, counts)
        