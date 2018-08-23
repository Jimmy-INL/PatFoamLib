#! /usr/bin/env python

# See http://www.openfoamworkshop.org/2009/4th_Workshop/0_Feature_Presentations/OFW4_2009_Gschaider_PyFoam.pdf slide 48

from PyFoam.Execution.UtilityRunner import UtilityRunner
from PyFoam.Execution.BasicRunner import BasicRunner
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from os import path
import os
import time
import csv
import sys
import shutil, errno
import subprocess
import logging
import datetime

logger = logging.getLogger(__name__)


def getU0(L1UfilePath, level):
    with open(L1UfilePath, 'rb') as f:
        mycsv = csv.reader(f,delimiter='\t')
        mycsv = list(mycsv)

        U0 = float(mycsv[level][1])
        print U0
        if U0 == 0.0:
            raise ValueError('Did not get the correct U0: %s' % U0)
    return U0

def udpdatePressureJump(pressurePath, dp0, dp1):
    #pnewTimePath = path.join( case ,str(endTime) + "/p")
    outletOld = '1((%s 0));' % dp0
    inletOld = 'jump            uniform %s;' % dp0

    outletNew = '1((%s 0));' % dp1
    inletNew = 'jump            uniform %s;' % dp1

    FullPath = os.getcwd()
    print FullPath

    FullPath = path.join( FullPath ,pressurePath )

    updateCommand = "sed 's/%s/%s/g' -i %s" % (outletOld, outletNew, FullPath)
    print updateCommand
    os.system(updateCommand)
    print updateCommand

    updateCommand = "sed 's/%s/%s/g' -i %s" % (inletOld, inletNew, FullPath)
    os.system(updateCommand)

    print updateCommand


def main(case, U0_Target, profile_name, level, runInterval=2):
    #case = "kOmegaSST_45_dy15_H14cm"

    dire = SolutionDirectory(case,archive=None,paraviewLink=False)

    dp0 = 0;
    dp1 = 0;
    U0_0 =0;
    U0_1 =0;

    #print 'pyFoamClearCase.py %s' % (dire)
    logger.info('Starting up, clearning the case.')
    os.system('pyFoamClearCase.py %s' % (case))


    # Read in the inital settings
    cntlDict = ParsedParameterFile( path.join( case ,"system/controlDict"))

    logger.info('    Updating the controlDict file.')
    startTime= 0
    cntlDict['startTime'] = startTime
    endTime = runInterval
    cntlDict['endTime'] = endTime
    cntlDict['writeInterval'] = runInterval
    cntlDict.writeFile()

    pressureFile = ParsedParameterFile( path.join( case ,str(startTime) + "/p"))

    logger.info('    Looking up the pressureDiff file')
    dp0 = pressureFile["pressureDiff"]

    # Read the current velocity
    L1UfilePath = path.join( case ,'postProcessing/sets',str(startTime), profile_name)
    logger.info("    Looking up: %s" % L1UfilePath)
    if os.path.isfile(L1UfilePath):
        U0_0 =getU0(L1UfilePath, level)
    else:
        raise ValueError('Could not find the velocity file: %s' % L1UfilePath)

    logger.info( '    Start time: %s' % startTime)
    logger.info( '    End time:  %s' % endTime)
    logger.info( '    pressureDiff: %s' % dp0)
    logger.info( '    U0_0: %s' % U0_0)
    logger.info( '    U0_Target: %s' % U0_Target)

    run=0

    while run < 10:

        # Run the model
        logger.info('-------------------------------------------------------------')
        logger.info('    Starting run of model.......RUN: %s' % run)
        logger.info('    Starting time: %s' % datetime.datetime.now())
        BasicRunner( argv =["pisoFoam","-case ", dire.name ], silent=True).start()
        logger.info('    Ending time: %s' % datetime.datetime.now())
        time.sleep(1)

        # Run the sample utility
        logger.info('    Extracting the velocity profile')
        sample_str = "sample -latestTime -case "
        sample_str += case
        os.system(sample_str)
        time.sleep(5)

        # Read the velocity
        L1UfilePath = path.join( case ,'postProcessing/sets',str(endTime), profile_name)
        U0_1 =getU0(L1UfilePath, level)
        logger.info('    The end velocity was: %s m/s, the target is: %s m/s' % (U0_1, U0_Target))


        # Adjust the pressure diff
        if run == 0:
            if U0_1 < U0_Target:
                logger.info("    U0 is too low %f, increasing pressure" % (U0_1))
                dp1 = dp0*1.05
            else:
                logger.info( "    U0 is too high %f, decreasing pressure" % (U0_1))
                dp1 = dp0*0.95

            U0_0 = U0_1
        else:
            logger.info( "    Calculating the pressure difference to get desired velocity")
            # Update the variables

            logger.info( "    dp0=%f dp1=%f U0_0=%f U0_1=%f" %(dp0, dp1, U0_0, U0_1))
            dpNew = dp0 + (U0_Target - U0_0)*((dp1-dp0)/(U0_1 - U0_0))
            if dpNew == 0:
                raise ValueException('dpNew is 0')
            U0_0 = U0_1
            dp0 = dp1
            dp1 = dpNew
            logger.info("    New difference is %f, old difference was, %f" %(dp1, dp0))

        # Update the pressure
        pressureFile = path.join( case ,str(endTime) + "/p")
        udpdatePressureJump(pressureFile, dp0, dp1)

        #Update the controlDict with the new start and end times
        startTime = endTime
        cntlDict['startTime'] = startTime
        endTime += runInterval
        cntlDict['endTime'] = endTime
        cntlDict.writeFile()

        run +=1
        logger.info('    End of loop')
        logger.info('-------------------------------------------------------------')


def testUpdatePressureJump():
    if os.path.isfile('channel.kwsst.rough.lowRe/p.test'):
        os.system('rm channel.kwsst.rough.lowRe/p.test')

    os.system('cp channel.kwsst.rough.lowRe/p.org channel.kwsst.rough.lowRe/p.test')

    dp0 = -0.005
    dp1 = dp0 * 1.05
    udpdatePressureJump('channel.kwsst.rough.lowRe/p.test', dp0, dp1)
    dp0 = dp1
    dp1 = dp0 * 1.05
    udpdatePressureJump('channel.kwsst.rough.lowRe/p.test', dp0, dp1)


if __name__ == "__main__":

    if (len(sys.argv) == 1) or (len(sys.argv) == 2):
        print "arg1: openfoam folder, arg2 is the target velocity"
    else:
        logger = logging.getLogger('')
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler('calibration_log.log')
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        logger.addHandler(fh)
        logger.addHandler(ch)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        profile_name = 'Dune6_12_U.xy'

        logger.info('-------------------------------------------------------------')
        logger.info('    Starting calibration run')
        logger.info('-------------------------------------------------------------')

        case = sys.argv[1]
        target_U = float(sys.argv[2])
        runinterval = 60
        if len(sys.argv) == 4:
            runinterval = int(sys.argv[3])
        logger.info('-------------------------------------------------------------')
        logger.info('    case: %s' % case)
        logger.info('    target U0: %s' % target_U)
        logger.info('    Run interval: % s' % runinterval)
        logger.info('    Start time: %s' % datetime.datetime.now())
        logger.info('    Profile Name: %s' % profile_name)
        logger.info('-------------------------------------------------------------')

        try:
            main(case, target_U, profile_name, 55, runinterval)
            '''L1UfilePath = path.join( case ,'postProcessing/sets',str(0), profile_name)'''
            ''' if os.path.isfile(L1UfilePath):
                U0 = getU0(L1UfilePath,55)
                print 'U0 = %s' % U0
            else:
                print 'Did not find path: %s' % L1UfilePath '''
        except:
            logger.exception('')

        logger.info('-------------------------------------------------------------')
        logger.info('    Calibration complete')
        logger.info('    Ending time: %s' % datetime.datetime.now())
        logger.info('-------------------------------------------------------------')



    #testUpdatePressureJump()
    '''
      if (len(sys.argv) == 1) or (len(sys.argv) == 2):
        print "arg1: openfoam folder, arg2 is the target velocity"
      else:
        main(sys.argv[1], sys.argv[2])'''

