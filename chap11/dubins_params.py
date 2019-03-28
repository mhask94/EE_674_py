# dubins_parameters
#   - Dubins parameters that define path between two configurations
#
# mavsim_matlab 
#     - Beard & McLain, PUP, 2012
#     - Update history:  
#         3/26/2019 - RWB

import numpy as np
import sys
sys.path.append('..')

class dubins_params:
    def __init__(self):
        self.p_s = np.inf*np.ones((3,1))  # the start position in re^3
        self.chi_s = np.inf  # the start course angle
        self.p_e = np.inf*np.ones((3,1))  # the end position in re^3
        self.chi_e = np.inf  # the end course angle
        self.radius = np.inf  # turn radius
        self.length = np.inf  # length of the Dubins path
        self.center_s = np.inf*np.ones((3,1))  # center of the start circle
        self.dir_s = np.inf  # direction of the start circle
        self.center_e = np.inf*np.ones((3,1))  # center of the end circle
        self.dir_e = np.inf  # direction of the end circle
        self.r1 = np.inf*np.ones((3,1))  # vector in re^3 defining half plane H1
        self.r2 = np.inf*np.ones((3,1))  # vector in re^3 defining position of half plane H2
        self.r3 = np.inf*np.ones((3,1))  # vector in re^3 defining position of half plane H3
        self.n1 = np.inf*np.ones((3,1))  # unit vector in re^3 along straight line path
        self.n3 = np.inf*np.ones((3,1))  # unit vector defining direction of half plane H3

    def update(self, ps, chis, pe, chie, R):
        ell = np.linalg.norm(ps[0:2] - pe[0:2])
        if ell < 2 * R:
            print('Error in Dubins Parameters: The distance between nodes must be larger than 2R.')
        else:
            Cxs = np.cos(chis)
            Sxs = np.sin(chis)
            Cxe = np.cos(chie)
            Sxe = np.sin(chie)
            c_rs = ps + R*rotz(np.pi/2) @ np.array([[Cxs,Sxs,0]]).T
            c_ls = ps + R*rotz(-np.pi/2) @ np.array([[Cxs,Sxs,0]]).T
            c_re = pe + R*rotz(np.pi/2) @ np.array([[Cxe,Sxe,0]]).T
            c_le = pe + R*rotz(-np.pi/2) @ np.array([[Cxe,Sxe,0]]).T
            # compute L1,L2,L3,L4
            L1 = np.linalg.norm(c_rs-c_re)+R*()#TODO finish this fn

            self.p_s = ps
            self.chi_s = chis
            self.p_e = pe
            self.chi_e = chie
            self.radius = R
            self.length = 0
            self.center_s = 0
            self.dir_s = 0
            self.center_e = 0
            self.dir_e = 0
            self.r1 = 0
            self.n1 = 0
            self.r2 = 0
            self.r3 = 0
            self.n3 = 0

def rotz(theta):
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                    [np.sin(theta), np.cos(theta), 0],
                    [0, 0, 1]])

def mod(x):
    return x % 2*np.pi
