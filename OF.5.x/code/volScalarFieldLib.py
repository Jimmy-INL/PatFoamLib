#!/usr/bin/python
'''
This library is designed to read volScalarField output.
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

def read_yPlus(filePath,wallname='bottomWall'):
    parsedyPlus = ParsedParameterFile(filePath)
    yPluses = parsedyPlus['boundaryField'][wallname]['value']

    yPluslist = []
    for yPlus in yPluses:
        yPluslist.append(float(yPlus))
    return np.array(yPluslist)


def read_boundary(filePath,wallname='bottomWall'):
    parsedfile = ParsedParameterFile(filePath)
    values = parsedfile['boundaryField'][wallname]['value']
    
    
    if values.isUniform() == False:
        valuelist = []
        for value in values:
            valuelist.append(float(value))
        return np.array(valuelist)
    else:
        return np.array(values.value())
        


def get_distance_along_wall(var, length):
    dx = length / var.size
    x = np.array([x*dx for x in range(var.size)])
    
    return x