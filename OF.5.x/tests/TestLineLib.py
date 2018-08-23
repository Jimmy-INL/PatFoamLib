import sys
sys.path.append("../code")
import unittest
import numpy as np
import SampleLineLib


class TestLineLib(unittest.TestCase):

    def setUp(self):
        self.ulinepath = 'data/lineL1_U.xy'
        self.turblinepath = 'data/lineL1_k_nut_omega.xy'
        self.rlinepath = 'data/lineL1_R.xy'

    def test_read_turb_line(self):
        turbdata = SampleLineLib.read_turb_line(self.turblinepath)
        kavg = np.average(turbdata.k)
        print 'The average k is: %s' % kavg

    def test_read_reynolds_line(self):
        rdata = SampleLineLib.read_reynolds_line(self.rlinepath)
        rXYavg = np.average(rdata.rXY)
        rXXavg = np.average(rdata.rXX)
        rXZZavg = np.average(rdata.rXZ)

        print 'The average rXYavg is: %s' % rXYavg
        print 'The average rXXavg is: %s' % rXXavg
        print 'The average rXZZavg is: %s' % rXZZavg

    def test_read_U_line(self):
        udata = SampleLineLib.read_U_line(self.ulinepath)
        uavg = np.average(udata.uX)
        print 'The average Ux is: %s' % uavg

    def test_calculate_average_velocity(self):
        udata = SampleLineLib.read_U_line(self.ulinepath)
        uavg = SampleLineLib.calculate_average_velocity(udata.uX, udata.y)
        print 'The average velocity: %s, the expected: 0.3393' % uavg



if __name__ == '__main__':
    unittest.main()

