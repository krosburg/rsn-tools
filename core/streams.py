# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 09:36:24 2019

@author: Kellen
"""

rdList = {
   "CE04OSBP-LJ01C-05-ADCPSI103": {
      "method": "streamed",
      "stream": "adcp_velocity_beam",
      "fullrd": "CE04OSBP/LJ01C/05-ADCPSI103",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "RS01SUM2-MJ01B-12-ADCPSK101": {
      "method": "streamed",
      "stream": "adcp_velocity_beam",
      "fullrd": "RS01SUM2/MJ01B/12-ADCPSK101",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "CE02SHBP-LJ01D-05-ADCPTB104": {
      "method": "streamed",
      "stream": "adcp_velocity_beam",
      "fullrd": "CE02SHBP/LJ01D/05-ADCPTB104",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "RS01SBPS-PC01A-05-ADCPTD102": {
      "method": "streamed",
      "stream": "adcp_velocity_beam",
      "fullrd": "RS01SBPS/PC01A/05-ADCPTD102",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "RS03AXPS-PC03A-05-ADCPTD302": {
      "method": "streamed",
      "stream": "adcp_velocity_beam",
      "fullrd": "RS03AXPS/PC03A/05-ADCPTD302",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "RS01SLBS-LJ01A-10-ADCPTE101": {
      "method": "streamed",
      "stream": "adcp_velocity_beam",
      "fullrd": "RS01SLBS/LJ01A/10-ADCPTE101",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "RS03AXBS-LJ03A-10-ADCPTE303": {
      "method": "streamed",
      "stream": "adcp_velocity_beam",
      "fullrd": "RS03AXBS/LJ03A/10-ADCPTE303",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "RS03CCAL-MJ03F-05-BOTPTA301": {
      "method": "streamed",
      "stream": "botpt_lily_sample",
      "fullrd": "RS03CCAL/MJ03F/05-BOTPTA301",
      "testPD": "PD839",
      "pdName": "lily_x_tilt"
   },
   "RS03ECAL-MJ03E-06-BOTPTA302": {
      "method": "streamed",
      "stream": "botpt_lily_sample",
      "fullrd": "RS03ECAL/MJ03E/06-BOTPTA302",
      "testPD": "PD839",
      "pdName": "lily_x_tilt"
   },
   "RS03INT2-MJ03D-06-BOTPTA303": {
      "method": "streamed",
      "stream": "botpt_lily_sample",
      "fullrd": "RS03INT2/MJ03D/06-BOTPTA303",
      "testPD": "PD839",
      "pdName": "lily_x_tilt"
   },
   "RS03ASHS-MJ03B-09-BOTPTA304": {
      "method": "streamed",
      "stream": "botpt_lily_sample",
      "fullrd": "RS03ASHS/MJ03B/09-BOTPTA304",
      "testPD": "PD839",
      "pdName": "lily_x_tilt"
   },
   "CE02SHBP-LJ01D-06-CTDBPN106": {
      "method": "streamed",
      "stream": "ctdbp_no_sample",
      "fullrd": "CE02SHBP/LJ01D/06-CTDBPN106",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "CE04OSBP-LJ01C-06-CTDBPO108": {
      "method": "streamed",
      "stream": "ctdbp_no_sample",
      "fullrd": "CE04OSBP/LJ01C/06-CTDBPO108",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "RS01SBPS-SF01A-2A-CTDPFA102": {
      "method": "streamed",
      "stream": "ctdpf_sbe43_sample",
      "fullrd": "RS01SBPS/SF01A/2A-CTDPFA102",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "RS01SBPS-PC01A-4A-CTDPFA103": {
      "method": "streamed",
      "stream": "ctdpf_optode_sample",
      "fullrd": "RS01SBPS/PC01A/4A-CTDPFA103",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "CE04OSPS-SF01B-2A-CTDPFA107": {
      "method": "streamed",
      "stream": "ctdpf_sbe43_sample",
      "fullrd": "CE04OSPS/SF01B/2A-CTDPFA107",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "CE04OSPS-PC01B-4A-CTDPFA109": {
      "method": "streamed",
      "stream": "ctdpf_optode_sample",
      "fullrd": "CE04OSPS/PC01B/4A-CTDPFA109",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "RS03AXPS-SF03A-2A-CTDPFA302": {
      "method": "streamed",
      "stream": "ctdpf_sbe43_sample",
      "fullrd": "RS03AXPS/SF03A/2A-CTDPFA302",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "RS03AXPS-PC03A-4A-CTDPFA303": {
      "method": "streamed",
      "stream": "ctdpf_optode_sample",
      "fullrd": "RS03AXPS/PC03A/4A-CTDPFA303",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "RS01SLBS-LJ01A-12-CTDPFB101": {
      "method": "streamed",
      "stream": "ctdpf_optode_sample",
      "fullrd": "RS01SLBS/LJ01A/12-CTDPFB101",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "RS03AXBS-LJ03A-12-CTDPFB301": {
      "method": "streamed",
      "stream": "ctdpf_optode_sample",
      "fullrd": "RS03AXBS/LJ03A/12-CTDPFB301",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },
   "RS03ASHS-MJ03B-10-CTDPFB304": {
      "method": "streamed",
      "stream": "ctdpf_optode_sample",
      "fullrd": "RS03ASHS/MJ03B/10-CTDPFB304",
      "testPD": "PD908",
      "pdName": "seawater_temperature"
   },           
   "RS01SLBS-LJ01A-12-DOSTAD101": {
      "method": "streamed",
      "stream": "do_stable_sample",
      "fullrd": "RS01SLBS/LJ01A/12-DOSTAD101",
      "testPD": "PD14",
      "pdName": "dissolved_oxygen"
   },
   "RS01SBPS-PC01A-4A-DOSTAD103": {
      "method": "streamed",
      "stream": "do_stable_sample",
      "fullrd": "RS01SBPS/PC01A/4A-DOSTAD103",
      "testPD": "PD14",
      "pdName": "dissolved_oxygen"
   },
   "CE02SHBP-LJ01D-06-DOSTAD106": {
      "method": "streamed",
      "stream": "do_stable_sample",
      "fullrd": "CE02SHBP/LJ01D/06-DOSTAD106",
      "testPD": "PD14",
      "pdName": "dissolved_oxygen"
   },
   "CE04OSBP-LJ01C-06-DOSTAD108": {
      "method": "streamed",
      "stream": "do_stable_sample",
      "fullrd": "CE04OSBP/LJ01C/06-DOSTAD108",
      "testPD": "PD14",
      "pdName": "dissolved_oxygen"
   },
   "CE04OSPS-PC01B-4A-DOSTAD109": {
      "method": "streamed",
      "stream": "do_stable_sample",
      "fullrd": "CE04OSPS/PC01B/4A-DOSTAD109",
      "testPD": "PD14",
      "pdName": "dissolved_oxygen"
   },
   "RS03AXBS-LJ03A-12-DOSTAD301": {
      "method": "streamed",
      "stream": "do_stable_sample",
      "fullrd": "RS03AXBS/LJ03A/12-DOSTAD301",
      "testPD": "PD14",
      "pdName": "dissolved_oxygen"
   },
   "RS03AXPS-PC03A-4A-DOSTAD303": {
      "method": "streamed",
      "stream": "do_stable_sample",
      "fullrd": "RS03AXPS/PC03A/4A-DOSTAD303",
      "testPD": "PD14",
      "pdName": "dissolved_oxygen"
   },
   "RS03INT1-MJ03C-07-D1000A301": {
      "method": "streamed",
      "stream": "d1000_sample",
      "fullrd": "RS03INT1/MJ03C/07-D1000A301",
      "testPD": "PD1048",
      "pdName": "temperature1"
   },           
   "RS01SBPS-PC01A-4C-FLORDD103": {
      "method": "streamed",
      "stream": "flort_d_data_record",
      "fullrd": "RS01SBPS/PC01A/4C-FLORDD103",
      "testPD": "PD22",
      "pdName": "fluorometric_chlorophyll_a"
   },
   "RS01SBPS-SF01A-3A-FLORTD101": {
      "method": "streamed",
      "stream": "flort_d_data_record",
      "fullrd": "RS01SBPS/SF01A/3A-FLORTD101",
      "testPD": "PD22",
      "pdName": "fluorometric_chlorophyll_a"
   },
   "CE04OSPS-SF01B-3A-FLORTD104": {
      "method": "streamed",
      "stream": "flort_d_data_record",
      "fullrd": "CE04OSPS/SF01B/3A-FLORTD104",
      "testPD": "PD22",
      "pdName": "fluorometric_chlorophyll_a"
   },
   "RS03AXPS-SF03A-3A-FLORTD301": {
      "method": "streamed",
      "stream": "flort_d_data_record",
      "fullrd": "RS03AXPS/SF03A/3A-FLORTD301",
      "testPD": "PD22",
      "pdName": "fluorometric_chlorophyll_a"
   },
   "RS03AXPS-PC03A-4C-FLORDD303": {
      "method": "streamed",
      "stream": "flort_d_data_record",
      "fullrd": "RS03AXPS/PC03A/4C-FLORDD303",
      "testPD": "PD22",
      "pdName": "fluorometric_chlorophyll_a"
   },
   "RS01SLBS-LJ01A-05-HPIESA101": {
      "method": "streamed",
      "stream": "echo_sounding",
      "fullrd": "RS01SLBS/LJ01A/05-HPIESA101",
     "testPD": "PD3780",
      "pdName": "hpies_travel_time1_L1"
   },
   "RS03AXBS-LJ03A-05-HPIESA301": {
      "method": "streamed",
      "stream": "echo_sounding",
      "fullrd": "RS03AXBS/LJ03A/05-HPIESA301",
      "testPD": "PD3780",
      "pdName": "hpies_travel_time1_L1"
   },
   "RS01SBPS-SF01A-4A-NUTNRA101": {
      "method": "streamed",
      "stream": "nutnr_a_sample",
      "fullrd": "RS01SBPS/SF01A/4A-NUTNRA101",
      "testPD": "PD315",
      "pdName": "nitrate_concentration"
   },
   "CE04OSPS-SF01B-4A-NUTNRA102": {
      "method": "streamed",
      "stream": "nutnr_a_sample",
      "fullrd": "CE04OSPS/SF01B/4A-NUTNRA102",
      "testPD": "PD315",
      "pdName": "nitrate_concentration"
   },
   "RS03AXPS-SF03A-4A-NUTNRA301": {
      "method": "streamed",
      "stream": "nutnr_a_sample",
      "fullrd": "RS03AXPS/SF03A/4A-NUTNRA301",
      "testPD": "PD315",
      "pdName": "nitrate_concentration"
   },
   "RS01SBPS-SF01A-3B-OPTAAD101": {
      "method": "streamed",
      "stream": "optaa_sample",
      "fullrd": "RS01SBPS/SF01A/3B-OPTAAD101",
      "testPD": "PD589",
      "pdName": "external_temp_raw"
   },
   "RS01SLBS-LJ01A-11-OPTAAC103": {
      "method": "streamed",
      "stream": "optaa_sample",
      "fullrd": "RS01SLBS/LJ01A/11-OPTAAC103",
      "testPD": "PD589",
      "pdName": "external_temp_raw"
   },
   "CE04OSBP-LJ01C-08-OPTAAC104": {
      "method": "streamed",
      "stream": "optaa_sample",
      "fullrd": "CE04OSBP/LJ01C/08-OPTAAC104",
      "testPD": "PD589",
      "pdName": "external_temp_raw"
   },
   "CE04OSPS-SF01B-3B-OPTAAD105": {
      "method": "streamed",
      "stream": "optaa_sample",
      "fullrd": "CE04OSPS/SF01B/3B-OPTAAD105",
      "testPD": "PD589",
      "pdName": "external_temp_raw"
   },
   "CE02SHBP-LJ01D-08-OPTAAD106": {
      "method": "streamed",
      "stream": "optaa_sample",
      "fullrd": "CE02SHBP/LJ01D/08-OPTAAD106",
      "testPD": "PD589",
      "pdName": "external_temp_raw"
   },
   "RS03AXPS-SF03A-3B-OPTAAD301": {
      "method": "streamed",
      "stream": "optaa_sample",
      "fullrd": "RS03AXPS/SF03A/3B-OPTAAD301",
      "testPD": "PD589",
      "pdName": "external_temp_raw"
   },
   "RS03AXBS-LJ03A-11-OPTAAC303": {
      "method": "streamed",
      "stream": "optaa_sample",
      "fullrd": "RS03AXBS/LJ03A/11-OPTAAC303",
      "testPD": "PD589",
      "pdName": "external_temp_raw"
   },
   "RS01SBPS-SF01A-3C-PARADA101": {
      "method": "streamed",
      "stream": "parad_sa_sample",
      "fullrd": "RS01SBPS/SF01A/3C-PARADA101",
      "testPD": "PD188",
      "pdName": "par"
   },
   "CE04OSPS-SF01B-3C-PARADA102": {
      "method": "streamed",
      "stream": "parad_sa_sample",
      "fullrd": "CE04OSPS/SF01B/3C-PARADA102",
      "testPD": "PD188",
      "pdName": "par"
   },
   "RS03AXPS-SF03A-3C-PARADA301": {
      "method": "streamed",
      "stream": "parad_sa_sample",
      "fullrd": "RS03AXPS/SF03A/3C-PARADA301",
      "testPD": "PD188",
      "pdName": "par"
   },
   "RS01SBPS-SF01A-4F-PCO2WA101": {
      "method": "streamed",
      "stream": "pco2w_a_sami_data_record",
      "fullrd": "RS01SBPS/SF01A/4F-PCO2WA101",
      "testPD": "PD931",
      "pdName": "pco2_seawater"
   },
   "CE04OSPS-SF01B-4F-PCO2WA102": {
      "method": "streamed",
      "stream": "pco2w_a_sami_data_record",
      "fullrd": "CE04OSPS/SF01B/4F-PCO2WA102",
      "testPD": "PD931",
      "pdName": "pco2_seawater"
   },
   "CE04OSPS-PC01B-4D-PCO2WA105": {
      "method": "streamed",
      "stream": "pco2w_a_sami_data_record",
      "fullrd": "CE04OSPS/PC01B/4D-PCO2WA105",
      "testPD": "PD931",
      "pdName": "pco2_seawater"
   },
   "RS03AXPS-SF03A-4F-PCO2WA301": {
      "method": "streamed",
      "stream": "pco2w_a_sami_data_record",
      "fullrd": "RS03AXPS/SF03A/4F-PCO2WA301",
      "testPD": "PD931",
      "pdName": "pco2_seawater"
   },
   "CE02SHBP-LJ01D-09-PCO2WB103": {
      "method": "streamed",
      "stream": "pco2w_b_sami_data_record",
      "fullrd": "CE02SHBP/LJ01D/09-PCO2WB103",
      "testPD": "PD931",
      "pdName": "pco2_seawater"
   },
   "CE04OSBP-LJ01C-09-PCO2WB104": {
      "method": "streamed",
      "stream": "pco2w_b_sami_data_record",
      "fullrd": "CE04OSBP/LJ01C/09-PCO2WB104",
      "testPD": "PD931",
      "pdName": "pco2_seawater"
   },
   "RS01SBPS-SF01A-2D-PHSENA101": {
      "method": "streamed",
      "stream": "phsen_data_record",
      "fullrd": "RS01SBPS/SF01A/2D-PHSENA101",
      "testPD": "PD939",
      "pdName": "ph_seawater"
   },
   "RS01SBPS-PC01A-4B-PHSENA102": {
      "method": "streamed",
      "stream": "phsen_data_record",
      "fullrd": "RS01SBPS/PC01A/4B-PHSENA102",
      "testPD": "PD939",
      "pdName": "ph_seawater"
   },
   "CE04OSPS-PC01B-4B-PHSENA106": {
      "method": "streamed",
      "stream": "phsen_data_record",
      "fullrd": "CE04OSPS/PC01B/4B-PHSENA106",
      "testPD": "PD939",
      "pdName": "ph_seawater"
   },
   "CE04OSPS-SF01B-2B-PHSENA108": {
      "method": "streamed",
      "stream": "phsen_data_record",
      "fullrd": "CE04OSPS/SF01B/2B-PHSENA108",
      "testPD": "PD939",
      "pdName": "ph_seawater"
   },
   "RS03AXPS-SF03A-2D-PHSENA301": {
      "method": "streamed",
      "stream": "phsen_data_record",
      "fullrd": "RS03AXPS/SF03A/2D-PHSENA301",
      "testPD": "PD939",
      "pdName": "ph_seawater"
   },
   "RS03AXPS-PC03A-4B-PHSENA302": {
      "method": "streamed",
      "stream": "phsen_data_record",
      "fullrd": "RS03AXPS/PC03A/4B-PHSENA302",
      "testPD": "PD939",
      "pdName": "ph_seawater"
   },
   "CE02SHBP-LJ01D-10-PHSEND103": {
      "method": "streamed",
      "stream": "phsen_data_record",
      "fullrd": "CE02SHBP/LJ01D/10-PHSEND103",
      "testPD": "PD939",
      "pdName": "ph_seawater"
   },
   "CE04OSBP-LJ01C-10-PHSEND107": {
      "method": "streamed",
      "stream": "phsen_data_record",
      "fullrd": "CE04OSBP/LJ01C/10-PHSEND107",
      "testPD": "PD939",
      "pdName": "ph_seawater"
   },
   "RS01SLBS-MJ01A-06-PRESTA101": {
      "method": "streamed",
      "stream": "prest_real_time",
      "fullrd": "RS01SLBS/MJ01A/06-PRESTA101",
      "testPD": "PD891",
      "pdName": "seafloor_pressure"
   },
   "RS03AXBS-MJ03A-06-PRESTA301": {
      "method": "streamed",
      "stream": "prest_real_time",
      "fullrd": "RS03AXBS/MJ03A/06-PRESTA301",
      "testPD": "PD891",
      "pdName": "seafloor_pressure"
   },
   "RS01SUM1-LJ01B-09-PRESTB102": {
      "method": "streamed",
      "stream": "prest_real_time",
      "fullrd": "RS01SUM1/LJ01B/09-PRESTB102",
      "testPD": "PD891",
      "pdName": "seafloor_pressure"
   },
   "RS01SBPS-SF01A-3D-SPKIRA101": {
      "method": "streamed",
      "stream": "spkir_data_record",
      "fullrd": "RS01SBPS/SF01A/3D-SPKIRA101",
      "testPD": "PD2645",
      "pdName": "spkir_downwelling_vector"
   },
   "CE04OSPS-SF01B-3D-SPKIRA102": {
      "method": "streamed",
      "stream": "spkir_data_record",
      "fullrd": "CE04OSPS/SF01B/3D-SPKIRA102",
      "testPD": "PD2645",
      "pdName": "spkir_downwelling_vector"
   },
   "RS03AXPS-SF03A-3D-SPKIRA301": {
      "method": "streamed",
      "stream": "spkir_data_record",
      "fullrd": "RS03AXPS/SF03A/3D-SPKIRA301",
      "testPD": "PD2645",
      "pdName": "spkir_downwelling_vector"
   },
   "RS03ASHS-MJ03B-07-TMPSFA301": {
      "method": "streamed",
      "stream": "tmpsf_sample",
      "fullrd": "RS03ASHS/MJ03B/07-TMPSFA301",
      "testPD": "PD2729",
      "pdName": "temperature17"
   },
   "RS03INT1-MJ03C-10-TRHPHA301": {
      "method": "streamed",
      "stream": "trhph_sample",
      "fullrd": "RS03INT1/MJ03C/10-TRHPHA301",
      "testPD": "PD431",
      "pdName": "resistivity_temp_degc"
   },
   "RS01SBPS-PC01A-06-VADCPA101": {
      "method": "streamed",
      "stream": "vadcp_velocity_beam",
      "fullrd": "RS01SBPS/PC01A/06-VADCPA101",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "RS03AXPS-PC03A-06-VADCPA301": {
      "method": "streamed",
      "stream": "vadcp_velocity_beam",
      "fullrd": "RS03AXPS/PC03A/06-VADCPA301",
      "testPD": "PD674",
      "pdName": "roll"
   },
   "RS01SLBS-MJ01A-12-VEL3DB101": {
      "method": "streamed",
      "stream": "vel3d_b_sample",
      "fullrd": "RS01SLBS/MJ01A/12-VEL3DB101",
      "testPD": "PD539",
      "pdName": "turbulent_velocity_east"
   },
   "RS01SUM1-LJ01B-12-VEL3DB104": {
      "method": "streamed",
      "stream": "vel3d_b_sample",
      "fullrd": "RS01SUM1/LJ01B/12-VEL3DB104",
      "testPD": "PD539",
      "pdName": "turbulent_velocity_east"
   },
   "RS03AXBS-MJ03A-12-VEL3DB301": {
      "method": "streamed",
      "stream": "vel3d_b_sample",
      "fullrd": "RS03AXBS/MJ03A/12-VEL3DB301",
      "testPD": "PD539",
      "pdName": "turbulent_velocity_east"
   },
   "RS03INT2-MJ03D-12-VEL3DB304": {
      "method": "streamed",
      "stream": "vel3d_b_sample",
      "fullrd": "RS03INT2/MJ03D/12-VEL3DB304",
      "testPD": "PD539",
      "pdName": "turbulent_velocity_east"
   },
   "CE04OSBP-LJ01C-07-VEL3DC107": {
      "method": "streamed",
      "stream": "vel3d_cd_velocity_data",
      "fullrd": "CE04OSBP/LJ01C/07-VEL3DC107",
      "testPD": "PD1085",
      "pdName": "vel3d_c_eastward_turbulent_velocity"
   },
   "CE02SHBP-LJ01D-07-VEL3DC108": {
      "method": "streamed",
      "stream": "vel3d_cd_velocity_data",
      "fullrd": "CE02SHBP/LJ01D/07-VEL3DC108",
      "testPD": "PD1085",
      "pdName": "vel3d_c_eastward_turbulent_velocity"
   },
   "RS01SBPS-SF01A-4B-VELPTD102": {
      "method": "streamed",
      "stream": "velpt_velocity_data",
      "fullrd": "RS01SBPS/SF01A/4B-VELPTD102",
      "testPD": "PD3230",
      "pdName": "velpt_d_eastward_velocity"
   },
   "CE04OSPS-SF01B-4B-VELPTD106": {
      "method": "streamed",
      "stream": "velpt_velocity_data",
      "fullrd": "CE04OSPS/SF01B/4B-VELPTD106",
      "testPD": "PD3230",
      "pdName": "velpt_d_eastward_velocity"
   },
   "RS03AXPS-SF03A-4B-VELPTD302": {
      "method": "streamed",
      "stream": "velpt_velocity_data",
      "fullrd": "RS03AXPS/SF03A/4B-VELPTD302",
      "testPD": "PD3230",
      "pdName": "velpt_d_eastward_velocity"
   }
}