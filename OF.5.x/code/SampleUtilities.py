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
import math

__density = 1000.
__mu = 1.e-3


def getFlowParametersAlongLine(U_path, gradU_path, turb_path, params={'k':1, 'nut':2,'omega':3}, 
    density=1000., mu=1.e-3, grad='rYX', base_elevation=None):
    
    # Load up the velocities
    uArray = SampleLineLib.read_U_line(U_path)
     
    # Load up the gradient
    gradUArray = SampleLineLib.read_gradU_line(gradU_path)
    
    # Load up the turbulent parameters
    turbArray = SampleLineLib.read_turb_line(turb_path, params=params)
    
    #wss = wss * -1.0 / (1000.*0.5*model['Ubulk']**2.)
    
    
    retvalDf = pd.DataFrame()
    retvalDf['Ux'] = pd.Series(uArray.uX, uArray.y)
    retvalDf['Uy'] = pd.Series(uArray.uY, uArray.y)
    retvalDf['Uz'] = pd.Series(uArray.uZ, uArray.y)
    if grad=='rYX':
        retvalDf['dUxdz'] = pd.Series(gradUArray.rYX, index=gradUArray.y)
    elif grad=='rZX':
        retvalDf['dUxdz'] = pd.Series(gradUArray.rZX, index=gradUArray.y)
    else:
         raise Exception('grad should be either rYX or rZX: {}'.format(x))
    retvalDf['nut'] = pd.Series(turbArray.nut, index=gradUArray.y)
    retvalDf['k'] = pd.Series(turbArray.k, index=gradUArray.y)
    retvalDf['omega'] = pd.Series(turbArray.omega, index=gradUArray.y)
    retvalDf['yref'] = pd.Series(gradUArray.y, index=gradUArray.y)    
    
    # Extract the bottom elevation - note that this will change depending on where the 
    # sample was extracted - currently set for the cell face. 
    if base_elevation is None:
        y0 = gradUArray.y[0]    
    else:
        y0 = base_elevation
    retvalDf['yref'] = retvalDf.apply(lambda row: row['yref'] - y0, axis=1)

    
    # Calculate mududy
    retvalDf['mududy'] = retvalDf.apply(lambda row: mu * row['dUxdz'], axis=1)
    
    # Calculate rhonutdudy
    retvalDf['rhonutdudy'] = retvalDf.apply(lambda row: density*row['nut']*row['dUxdz'], axis=1)
    
    # Calculate the nueffdudy
    retvalDf['nueffdudy'] = retvalDf.apply(lambda row: (mu + density*row['nut'])*row['dUxdz'], axis=1)

    tau_bed = retvalDf.iloc[0].nueffdudy
    print(tau_bed)
    ustar = math.sqrt(abs(tau_bed)/density)
    
    retvalDf['yplus'] = retvalDf.apply(lambda row: ustar*row['yref']/(mu/density), axis=1)
    
    return retvalDf
    
    
    

'''
This gets the flow parameters along a path (in the x-dir)
'''
def getFlowParametersAlongPath(gradU_path, turb_path, params={'k':1, 'nut':2,'omega':3}, density=1000., mu=1.e-3):                                                                                 
                                                                                 
    gradUArray = SamplePathLib.read_gradU_path(gradU_path)    
    turbArray = SamplePathLib.read_turb_path(turb_path, params=params)

    retvalDf = pd.DataFrame()
    
    retvalDf['dUxdz'] = pd.Series(gradUArray.rZX, index=gradUArray.x)
    retvalDf['nut'] = pd.Series(turbArray.nut, index=gradUArray.x)
    retvalDf['k'] = pd.Series(turbArray.k, index=gradUArray.x)
    retvalDf['omega'] = pd.Series(turbArray.omega, index=gradUArray.x)

    retvalDf['neff'] = retvalDf.apply(lambda row: row['nut']*density + mu, axis=1)
    retvalDf['shear'] = retvalDf.apply(lambda row: row['neff'] * row['dUxdz'], axis=1)

    return retvalDf


def getUProfile(modelpath, timestep,profile, prefix='lineL'):
    filePathTemplate = '{0}/postProcessing/sets/{1}/{2}{3}_U.xy'.format(modelpath, timestep, prefix, profile)
    if os.path.exists(filePathTemplate) == False:
        filePathTemplate = '{0}/postProcessing/sampleDict/{1}/{2}{3}_U.xy'.format(modelpath, timestep, prefix, profile)
    
    modelResult = SampleLineLib.read_U_line(filePathTemplate)
    return modelResult
    


def getRProfile(modelpath,timestep,profile,prefix='lineL'):
    filePathTemplate = '{0}/postProcessing/sets/{1}/{2}{3}_R.xy'.format(modelpath, timestep, prefix, profile)
    if os.path.exists(filePathTemplate) == False:
        filePathTemplate = '{0}/postProcessing/sampleDict/{1}/{2}{3}_R.xy'.format(modelpath, timestep, prefix, profile)
    
    if os.path.exists(filePathTemplate) == False:
        filePathTemplate = '{0}/postProcessing/sets/{1}/{2}{3}_turbulenceProperties:R.xy'.format(modelpath, timestep, prefix, profile)
        if os.path.exists(filePathTemplate) == False:
            filePathTemplate = '{0}/postProcessing/sampleDict/{1}/{2}{3}_turbulenceProperties:R.xy'.format(modelpath, timestep, prefix, profile)
    
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
