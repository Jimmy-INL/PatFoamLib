
#!/usr/bin/python
'''
This is a module specific functions for calculating dimensionless numbers
'''
__author__ = "Patrick Grover"
__copyright__ = ""
__credits__ = ["Patrick Grover"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Patrick Grover"
__email__ = ""
__status__ = "Development"


def get_knplus(ustar,kn, ismm=True):
    nu = 1e-6
    kn_ = kn
    if ismm == True:
        kn_ = kn_/1000
    knplus = ustar*kn_/nu
    return knplus
