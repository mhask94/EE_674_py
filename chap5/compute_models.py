"""
compute_ss_model
    - Chapter 5 assignment for Beard & McLain, PUP, 2012
    - Update history:  
        2/4/2019 - RWB
"""
import sys
sys.path.append('..')
import numpy as np
from scipy.optimize import minimize
from tools.tools import Euler2Quaternion, Quaternion2Euler
#from tools.transfer_function import transfer_function
from control import TransferFunction as TF
import params.aerosonde_params as MAV
from params.sim_params import ts_simulation as Ts

def compute_tf_model(mav, trim_state, trim_input):
    # trim values
    rho = MAV.rho
    Va = mav._Va
    S = MAV.S_wing
    b = MAV.b
    c = MAV.c
    Cpp = MAV.C_p_p
    Cpb = MAV.C_p_beta
    Cp0 = MAV.C_p_0
    b_2Va = b / (2*Va)

    a_phi_1 = 0.5 * rho * (Va**2) * S * b * Cpp * b_2Va
    a_phi_2 = 0.5 * rho * (Va**2) * S * b * MAV.C_p_delta_a
#    d_phi_2 = MAV.gamma1
#    T_phi_delta_a


    return T_phi_delta_a, T_chi_phi, T_theta_delta_e, T_h_theta, T_h_Va, T_Va_delta_t, T_Va_theta, T_beta_delta_r

def compute_ss_model(mav, trim_state, trim_input):
     return A_lon, B_lon, A_lat, B_lat

def euler_state(x_quat):
    # convert state x with attitude represented by quaternion
    # to x_euler with attitude represented by Euler angles
     return x_euler

def quaternion_state(x_euler):
    # convert state x_euler with attitude represented by Euler angles
    # to x_quat with attitude represented by quaternions
    return x_quat

def f_euler(mav, x_euler, input):
    # return 12x1 dynamics (as if state were Euler state)
    # compute f at euler_state
    return f_euler_

def df_dx(mav, x_euler, input):
    # take partial of f_euler with respect to x_euler
    return A

def df_du(mav, x_euler, delta):
    # take partial of f_euler with respect to delta
    return B

def dT_dVa(mav, Va, delta_t):
    # returns the derivative of motor thrust with respect to Va
    return dThrust

def dT_ddelta_t(mav, Va, delta_t):
    # returns the derivative of motor thrust with respect to delta_t
    return dThrust
