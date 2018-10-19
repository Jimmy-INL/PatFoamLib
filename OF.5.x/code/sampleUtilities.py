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
import SamplePathLib
import pandas as pd

__density = 1000.
__mu = 1.e-3


def getFlowParametersAlongPath(modelPath, timestep, SamplePathPrefix, params={'k':1, 'nut':2,'omega':3}):


    filePathTemplate = '{0}/postProcessing/sampleDict/{1}/{2}_grad(U).xy'.format(modelPath,
                                                                                 timestep, SamplePathPrefix)
    gradUArray = SamplePathLib.read_gradU_path(filePathTemplate)

    filePathTemplate = '{0}/postProcessing/sampleDict/{1}/{2}_k_omega_nut.xy'.format(modelPath,
                                                                                 timestep, SamplePathPrefix)
    turbArray = SamplePathLib.read_turb_path(filePathTemplate, params=params)

    retvalDf = pd.DataFrame()

    retvalDf['dUxdz'] = pd.Series(gradUArray.rZX, index=gradUArray.x)
    retvalDf['nut'] = pd.Series(turbArray.nut, index=gradUArray.x)
    retvalDf['k'] = pd.Series(turbArray.k, index=gradUArray.x)
    retvalDf['omega'] = pd.Series(turbArray.omega, index=gradUArray.x)

    retvalDf['neff'] = retvalDf.apply(lambda row: row['nut']*__density + __mu, axis=1)
    retvalDf['shear'] = retvalDf.apply(lambda row: row['neff'] * row['dUxdz'], axis=1)

    return retvalDf














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
