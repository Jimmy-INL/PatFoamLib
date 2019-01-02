#!/usr/bin/python
'''
This library is designed to read path data extracted using the sampleDict in
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

class turb_path():
    def __init__(self):
      self.k=[]
      self.omega=[]
      self.epsilon=[]
      self.nut=[]
      self.x=[]

class gradU_path(object):
    def __init__(self):
      self.rXX=[]
      self.rXY=[]
      self.rXZ=[]
      
      self.rYX=[]
      self.rYY=[]
      self.rYZ=[]

      self.rZX=[]
      self.rZY=[]
      self.rZZ=[]     

      self.x=[]

'''
======================= Utilities ============================
'''


def read_turb_path(filePath, starting_param = 1, params={'k':1, 'nut':2,'omega':3}):
    '''
    TODO make more robust by parsing the different parameters from the
    file name, currently it is hard coded for k, nut, omega.
    '''
    #base = os.path.basename(filePath)
    #params = os.path.splitext(base)
    #params= params.split('_')

    fil = open(filePath,'r')
    retval = turb_path()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(' \t')]
      retval.x.append(float(row[0]))
      retval.k.append(float(row[params['k']]))
      retval.nut.append(float(row[params['nut']]))
      retval.omega.append(float(row[params['omega']]))
    return retval



'''
-----------grad.H-------------------------- 
https://www.cfd-online.com/Forums/openfoam-programming-development/90467-output-velocity-gradients.html

volScalarField X=U.component(0); 
volScalarField Y=U.component(1); 
volScalarField Z=U.component(2); 
 
 
volScalarField XX=gradU.component(0); 
volScalarField YY=gradU.component(4); 
volScalarField ZZ=gradU.component(8); 
 
volScalarField XY=gradU.component(1); 
volScalarField YZ=gradU.component(5); 
volScalarField ZX=gradU.component(6); 
 
volScalarField YX=gradU.component(3); 
volScalarField ZY=gradU.component(7); 
volScalarField XZ=gradU.component(2); 
  
Variable = X*XX + … ## 
'''
def read_gradU_path(filePath):
    
    fil = open(filePath,'r')
    retval = gradU_path()
    for line in fil:
      row = [x.strip(' \t\n\r') for x in line.split(' \t')]
      retval.x.append(float(row[0]))
      retval.rXX.append(float(row[1]))
      retval.rXY.append(float(row[2]))
      retval.rXZ.append(float(row[3]))
      
      retval.rYX.append(float(row[4]))
      retval.rYY.append(float(row[5]))
      retval.rYZ.append(float(row[6]))

      retval.rZX.append(float(row[7]))
      retval.rZY.append(float(row[8]))
      retval.rZZ.append(float(row[9]))

    return retval



