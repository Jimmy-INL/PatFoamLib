#!/usr/bin/python
'''
This library is designed to assist in setting up profile plots.
'''

__author__ = "Patrick Grover"
__copyright__ = ""
__credits__ = ["Patrick Grover"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Patrick Grover"
__email__ = ""
__status__ = "Development"

import sys
import os
import SampleLineLib

def getUProfile(modelpath,timestep,profile):
    filePathTemplate = '{0}/postProcessing/sets/{1}/lineL{2}_U.xy'.format(modelpath, timestep, profile)
    if os.path.exists(filePathTemplate) == False:
        filePathTemplate = '{0}/postProcessing/sampleDict/{1}/lineL{2}_U.xy'.format(modelpath, timestep, profile)
    
    modelResult = SampleLineLib.read_U_line(filePathTemplate)
    return modelResult

def getRProfile(modelpath,timestep,profile):
    filePathTemplate = '{0}/postProcessing/sets/{1}/lineL{2}_R.xy'.format(modelpath, timestep, profile)
    if os.path.exists(filePathTemplate) == False:
        filePathTemplate = '{0}/postProcessing/sampleDict/{1}/lineL{2}_R.xy'.format(modelpath, timestep, profile)
    
    if os.path.exists(filePathTemplate) == False:
        filePathTemplate = '{0}/postProcessing/sets/{1}/lineL{2}_turbulenceProperties:R.xy'.format(modelpath, timestep, profile)
        if os.path.exists(filePathTemplate) == False:
            filePathTemplate = '{0}/postProcessing/sampleDict/{1}/lineL{2}_turbulenceProperties:R.xy'.format(modelpath, timestep, profile)
    
    modelResult = SampleLineLib.read_reynolds_line(filePathTemplate)
    return modelResult


def profileMean( U,Z ):
    SumWx = 0.
    SumW = 0.
    
    for i in range(2,len(Z)-1):
        dh1 = Z[i+1]-Z[i]
        if i< len(Z):
            dh2 = Z[i]-Z[i-1]
        else:
            dh2 = 0.
        
        dh = dh1/2. + dh2/2.
        
        SumW = SumW + dh
        SumWx = SumWx + U[i]*dh
        
    return SumWx/SumW
