import sys
sys.path.append("../code")
import unittest
import numpy as np
import volScalarFieldLib

class TestVolScalarFieldLib(unittest.TestCase):

    def setUp(self):
        print 'Hello2'
        self.ypluspath = 'data/yPlus'

    def test_read_yPlus(self):
        print 'Hello'
        yplus =volScalarFieldLib.read_yPlus(self.ypluspath)
        avgyplus = np.average(yplus)
        print "The average y+ is: %s" % avgyplus



if __name__ == '__main__':
    unittest.main()
