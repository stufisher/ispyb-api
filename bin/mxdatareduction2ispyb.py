#!/usr/bin/env python
# mxdatareduction2ispyb.py
#
#    Copyright (C) 2014 Diamond Light Source, Karl Levik
#
# 2015-01-05
#
# Script to store e.g. xia2 and fast_dp results using the ispyb_api.
#

import os
import sys
from datetime import datetime

import ispyb.factory
from ispyb.xmltools import mx_data_reduction_to_ispyb, xml_file_to_dict

if len(sys.argv) not in (3,4):
    print("Usage:")
    print("%s conf_file xml_in_file" % sys.argv[0])
    print("%s conf_file xml_in_file xml_out_file" % sys.argv[0])
    sys.exit(1)

conf_file = sys.argv[1]

conn = ispyb.factory.create_connection(conf_file)
mxprocessing = ispyb.factory.create_data_area(ispyb.factory.DataAreaType.MXPROCESSING, conn)

xml_file = sys.argv[2]
xml_dir = os.path.split(xml_file)[0]
# Find the datacollection associated with this data reduction run
try:
    dc_id = int(open(os.path.join(xml_dir, '.dc_id'), 'r').read())
    print('Got DC ID %d from file system' % dc_id)
except:
    dc_id = None

mx_data_reduction_dict = xml_file_to_dict(xml_file)
(app_id, ap_id, scaling_id, integration_id) = mx_data_reduction_to_ispyb(mx_data_reduction_dict, dc_id, mxprocessing)

# Write results to xml_out_file
if len(sys.argv) > 3:
    xml = '<?xml version="1.0" encoding="ISO-8859-1"?>'\
        '<dbstatus><autoProcProgramId>%d</autoProcProgramId>'\
        '<autoProcId>%d</autoProcId>'\
        '<autoProcScalingId>%d</autoProcScalingId>'\
        '<autoProcIntegrationId>%d</autoProcIntegrationId>'\
        '<code>ok</code></dbstatus>' % (app_id, ap_id, scaling_id, integration_id)
    f = open(sys.argv[3], 'w')
    f.write(xml)
    f.close()
