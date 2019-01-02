#!/usr/bin/python
'''
This library is designed to read volVectorField output.
'''

__author__ = "Patrick Grover"
__copyright__ = ""
__credits__ = ["Patrick Grover"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Patrick Grover"
__email__ = ""
__status__ = "Development"

import os
import numpy as np
import math
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile


def read_wallshearstress(filePath,wallname='bottomWall',shearid=0, density=1000.):
    ''' 
    NOTE: Need to include density to fully determine the shear stress 
    '''
    shear = ParsedParameterFile(filePath)
    wallValues = shear['boundaryField'][wallname]['value']
    shearlist = []
    for val in wallValues:
        shearlist.append(float(val[shearid])*density)
    return np.array(shearlist)

def calculate_ustar(wallshearstress, density=1000.):
    '''
    @param wallshearstress: List of shear stresses
    '''
    ustar = math.sqrt(abs(np.median(wallshearstress))/density)
    return ustar

