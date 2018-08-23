#!/usr/bin/python
'''
This library is designed to read line data extracted using the sampleDict in
OpenFOAM.
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

'''
======================= Entity Classes ============================
'''

class turb_line():
    def __init__(self):
      self.k=[]
      self.omega=[]
      self.epsilon=[]
      self.nut=[]
      self.y=[]

class u_line(object):
    def __init__(self):
      self.uX=[]
      self.uY=[]
      self.uZ=[]
      self.y=[]

class r_line(object):
    def __init__(self):
      self.rXX=[]
      self.rYY=[]
      self.rZZ=[]
      self.rXY=[]
      self.rXZ=[]
      self.rYZ=[]
      self.y=[]
'''
======================= Utilities ============================
'''

def read_turb_line(filePath, starting_param = 1, params={'k':1, 'nut':2,'omega':3}):
    '''
    TODO make more robust by parsing the different parameters from the
    file name, currently it is hard coded for k, nut, omega.
    '''
    #base = os.path.basename(filePath)
    #params = os.path.splitext(base)
    #params= params.split('_')

    fil = open(filePath,'r')
    retval = turb_line()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(' \t')]
      retval.y.append(float(row[0]))
      retval.k.append(float(row[params['k']]))
      retval.nut.append(float(row[params['nut']]))
      retval.omega.append(float(row[params['omega']]))
    return retval

def read_reynolds_line(filePath):
    '''Rxx, Rxy, Rxz, Ryy, Ryz and Rzz correspond to R(0), R(3), R(4), R(1), R(5) and R(2) respectively.'''
    fil = open(filePath,'r')
    retval = r_line()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(' \t')]
      retval.y.append(float(row[0]))
      retval.rXX.append(float(row[1]))
      retval.rYY.append(float(row[2]))
      retval.rZZ.append(float(row[3]))
      retval.rXY.append(float(row[4]))
      retval.rXZ.append(float(row[5]))
      retval.rYZ.append(float(row[6]))
    return retval

def read_U_line(filePath):
    fil = open(filePath,'r')
    retval = u_line()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(' \t')]
      retval.y.append(float(row[0]))
      retval.uX.append(float(row[1]))
      retval.uY.append(float(row[2]))
      retval.uZ.append(float(row[3]))
    return retval

def calculate_average_velocity(U,Z):
    sumU = 0
    sumZ = 0

    for i in range(1,len(Z)):
        dZ = Z[i] - Z[i-1]
        sumU += 0.5 * (U[i] + U[i-1]) * dZ
        sumZ += dZ

    return sumU/sumZ


