import sys
sys.path.append("../code")
import unittest
import numpy as np
import volVectorFieldLib

class TestVolVectorFieldLib(unittest.TestCase):

    def setUp(self):
        print 'Hello2'
        self.wsspath = '/home/geeko/working/Paper_4_Turbulence_Modelling/FlumeExperiment/channel.rough.rigid.30/450/wallShearStress'

    def test_read_wallshearstress(self):
        print 'Hello'
        wss =volVectorFieldLib.read_wallshearstress(self.wsspath)
        avgwss = np.average(wss)
        print "The average wall shear stress is: %s" % avgwss

    def test_calculate_ustar(self):
        wss =volVectorFieldLib.read_wallshearstress(self.wsspath)
        ustar = volVectorFieldLib.calculate_ustar(wss)

        print 'The calculated ustar is: %s' % ustar


if __name__ == '__main__':
    unittest.main()
