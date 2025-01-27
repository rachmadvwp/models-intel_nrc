# INTEL CORPORATION CONFIDENTIAL AND PROPRIETARY
# 
# Copyright © 2019-2021 Intel Corporation.
# 
# This software and the related documents are Intel copyrighted
# materials, and your use of them is governed by the express 
# license under which they were provided to you (License). Unless
# the License provides otherwise, you may not use, modify, copy, 
# publish, distribute, disclose or transmit  this software or the
# related documents without Intel's prior written permission.
# 
# This software and the related documents are provided as is, with
# no express or implied warranties, other than those that are 
# expressly stated in the License.

"""Handles reading the NMNIST dataset from files"""

import numpy as np
import os
import inspect
from attrdict import AttrDict

class Event():
    """A class to hold events
    """
    def __init__(self, filename):
        
        with open(filename, 'rb') as fileHandle:
            rawData = np.fromfile(fileHandle, dtype=np.uint8).astype('uint')
        
        self.x = rawData[0::5]
        self.y = rawData[1::5]
        self.p = rawData[2::5]>>7
        self.p -= np.min(self.p)
        self.t = ( (rawData[2::5]<<16) | (rawData[3::5]<<8) | (rawData[4::5]) ) & 0x7FFFFF
        self.t = self.t//1000

        
class NmnistDataset():
    """Interface to NMNIST dataset
    """
    def __init__(self, path):
        self.path = path
        self.labels = np.loadtxt(self.path+'/labels.txt').astype(int)
        self.sampleLength = 350

    def __getitem__(self, index):
        filename = self.path + '/' + str(index+1).zfill(5) + '.bin'
        data = Event(filename)
        events = AttrDict()
        events.x = data.x
        events.y = data.y
        events.t = data.t
        events.p = data.p
        return events

    def __len__(self):
        return len(self.labels)