from tkinter import filedialog
from tkinter import *
from math import *
from time import time

coeff_base = [
'fz',
'camber',
'aos',
'FZ0',
]

coeff_fy = [
'PCY1',
'PDY1','PDY2','PDY3',
'PEY1','PEY2','PEY3','PEY4',
'PKY1','PKY2','PKY3',
'PHY1','PHY2','PHY3',
'PVY1','PVY2','PVY3','PVY4',
]

coeff_fx = [
'PCX1',
'PDX1','PDX2',
'PEX1','PEX2','PEX3','PEX4',
'PKX1','PKX2','PKX3',
'PHX1','PHX2',
'PVX1','PVX2',
]

coeff_mz = [
'QBZ1','QBZ2','QBZ3','QBZ4','QBZ5',
'QCZ1',
'QDZ1','QDZ2','QDZ3','QDZ4',
'QEZ1','QEZ2','QEZ3','QEZ4','QEZ5',
'QHZ1','QHZ2','QHZ3','QHZ4',
'QBZ9','QBZ10',
'QDZ6','QDZ7','QDZ8','QDZ9',
]

coeff_fxy = [
'RBY1','RBY2','RBY3',
'RCY1',
'RHY1',
'RVY1','RVY2','RVY3','RVY4','RVY5','RVY6',
'RBX1','RBX2',
'RCX1',
'RHX1',
]

coeff_min = {
# Base parameters
'fz':500,
'camber':-8.0,
'aos':2.0,
'FZ0':1000,
# Lateral force
'PCY1':0.5,
'PDY1':0,
'PDY2':-0.5,
'PDY3':-5,
'PEY1':-5,
'PEY2':-0.5,
'PEY3':-0.5,
'PEY4':-50,
'PKY1':-50,
'PKY2':-5,
'PKY3':-0.5,
'PHY1':-0.5,
'PHY2':-0.5,
'PHY3':-0.5,
'PVY1':-0.5,
'PVY2':-0.5,
'PVY3':-0.5,
'PVY4':-0.5,
# Longitudinal force
'PCX1':0.5,
'PDX1':0,
'PDX2':-0.5,
'PEX1':-0.5,
'PEX2':-5,
'PEX3':-5,
'PEX4':-5,
'PKX1':10,
'PKX2':-25,
'PKX3':-5,
'PHX1':-0.5,
'PHX2':-0.5,
'PVX1':-0.5,
'PVX2':-0.5,
# Aligning moment
'QBZ1':-50,
'QBZ2':-50,
'QBZ3':-50,
'QBZ4':-5,
'QBZ5':-0.5,
'QCZ1':-5,
'QDZ1':-0.5,
'QDZ2':-0.5,
'QDZ3':-0.5,
'QDZ4':-5,
'QEZ1':-5,
'QEZ2':-5,
'QEZ3':-5,
'QEZ4':-5,
'QEZ5':-5,
'QHZ1':-0.5,
'QHZ2':-0.5,
'QHZ3':-0.5,
'QHZ4':-0.5,
'QBZ9':-50,
'QBZ10':-50,
'QDZ6':-0.5,
'QDZ7':-0.5,
'QDZ8':-0.5,
'QDZ9':-0.5,
# Lateral combined
'RBY1':-50,
'RBY2':-50,
'RBY3':-0.5,
'RCY1':-5,
'RHY1':-0.5,
'RVY1':-5,
'RVY2':-5,
'RVY3':-5,
'RVY4':-50,
'RVY5':-0.5,
'RVY6':-0.5,
# Longitudinal combined
'RBX1':-50,
'RBX2':-50,
'RCX1':-5,
'RHX1':-0.5,
}

coeff_max = {
# Base parameters
'fz':8500,
'camber':8.0,
'aos':30.0,
'FZ0':5000,
# Lateral force
'PCY1':2,
'PDY1':2,
'PDY2':0.5,
'PDY3':5,
'PEY1':5,
'PEY2':0.5,
'PEY3':0.5,
'PEY4':50,
'PKY1':50,
'PKY2':5,
'PKY3':0.5,
'PHY1':0.5,
'PHY2':0.5,
'PHY3':0.5,
'PVY1':0.5,
'PVY2':0.5,
'PVY3':0.5,
'PVY4':0.5,
# Longitudinal force
'PCX1':2,
'PDX1':2,
'PDX2':0.5,
'PEX1':0.5,
'PEX2':2,
'PEX3':5,
'PEX4':5,
'PKX1':50,
'PKX2':25,
'PKX3':5,
'PHX1':0.5,
'PHX2':0.5,
'PVX1':0.5,
'PVX2':0.5,
# Aligning moment
'QBZ1':50,
'QBZ2':50,
'QBZ3':50,
'QBZ4':5,
'QBZ5':0.5,
'QCZ1':5,
'QDZ1':0.5,
'QDZ2':0.5,
'QDZ3':0.5,
'QDZ4':5,
'QEZ1':5,
'QEZ2':5,
'QEZ3':5,
'QEZ4':5,
'QEZ5':5,
'QHZ1':0.5,
'QHZ2':0.5,
'QHZ3':0.5,
'QHZ4':0.5,
'QBZ9':50,
'QBZ10':50,
'QDZ6':0.5,
'QDZ7':0.5,
'QDZ8':0.5,
'QDZ9':0.5,
# Lateral combined
'RBY1':50,
'RBY2':50,
'RBY3':0.5,
'RCY1':5,
'RHY1':0.5,
'RVY1':5,
'RVY2':5,
'RVY3':5,
'RVY4':50,
'RVY5':0.5,
'RVY6':0.5,
# Longitudinal combined
'RBX1':50,
'RBX2':50,
'RCX1':5,
'RHX1':0.5,
}

coeff_default = {
# Base parameters
'fz':3000,
'camber':0.0,
'aos':8.0,
'FZ0':4500,
# Lateral force
'PCY1':1.27676,
'PDY1':0.9327755,
'PDY2':-0.128085,
'PDY3':1.019803,
'PEY1':-1.39934,
'PEY2':-0.074863,
'PEY3':0.17886,
'PEY4':-8.252847,
'PKY1':-17.361823,
'PKY2':2.2938964,
'PKY3':-0.110362,
'PHY1':0.0016966,
'PHY2':0.0038829,
'PHY3':0.0398737,
'PVY1':0.0069311,
'PVY2':0.0186856,
'PVY3':-0.061575,
'PVY4':-0.098064,
# Longitudinal force
'PCX1':1.3970897,
'PDX1':1.1020679,
'PDX2':-0.185241,
'PEX1':-0.459255,
'PEX2':-1.499501,
'PEX3':-2.469645,
'PEX4':-0.906741,
'PKX1':38.5031,
'PKX2':2.03196,
'PKX3':-0.591086,
'PHX1':-0.00227143,
'PHX2':0.00193555,
'PVX1':0.0575923,
'PVX2':-0.0287496,
# Aligning moment
'QBZ1':10.47871,
'QBZ2':-2.04739,
'QBZ3':6.09958,
'QBZ4':0.39191,
'QBZ5':-0.01279,
'QCZ1':1.18899,
'QDZ1':0.11411,
'QDZ2':0.00479,
'QDZ3':0.12582,
'QDZ4':-1.10927,
'QEZ1':-2.88862,
'QEZ2':-0.83490,
'QEZ3':3.71462,
'QEZ4':0.15337,
'QEZ5':1.33032,
'QHZ1':0.00024,
'QHZ2':0.00102,
'QHZ3':0.12610,
'QHZ4':0.01917,
'QBZ9':17.87469,
'QBZ10':5.66140,
'QDZ6':-0.00049,
'QDZ7':0.00025,
'QDZ8':-0.18840,
'QDZ9':0.00415,
# Lateral combined
'RBY1':11.14388,
'RBY2':10.14162,
'RBY3':-0.015481,
'RCY1':1.038732,
'RHY1':0.0031137,
'RVY1':-1.485137,
'RVY2':-4.425144,
'RVY3':0.680957,
'RVY4':10.72882,
'RVY5':-0.201998,
'RVY6':0.083549,
# Longitudinal combined
'RBX1':24.8565,
'RBX2':22.43545,
'RCX1':1.00542,
'RHX1':0.00344,
}

coeff_info = {
# Base parameters
'fz':'Current tire load [N]',
'camber':'Current camber [deg]',
'aos':'Current angle of slip [deg]',
'FZ0':'Nominal tire load Fznom [N]',
# Lateral force
'PCY1':'Lateral force shape factor Cy',
'PDY1':'Lateral friction uy',
'PDY2':'Lateral friction variation with load',
'PDY3':'Lateral friction variation with square camber',
'PEY1':'Lateral curvature Ey at Fznom',
'PEY2':'Lateral curvature variation with load',
'PEY3':'Zero order camber dependency of lateral curvature',
'PEY4':'Lateral curvature variation with camber',
'PKY1':'Stiffness maximum Ky / Fznom',
'PKY2':'Load at which stiffness maximum is reached',
'PKY3':'Stiffness maximum variation with camber',
'PHY1':'Horizontal shift Shy at Fznom',
'PHY2':'Horizontal shift variation with load',
'PHY3':'Horizontal shift variation with camber',
'PVY1':'Vertical shift Svy / Fz at Fznom',
'PVY2':'Vertical shift variation with load',
'PVY3':'Vertical shift variation with camber',
'PVY4':'Vertical shift variation with camber and load',
# Longitudinal force
'PCX1':'Longitudinal force shape factor Cx',
'PDX1':'Longitudinal friction ux at Fznom',
'PDX2':'Longitudinal friction variation with load',
'PEX1':'Longitudinal curvature Ex at Fznom',
'PEX2':'Longitudinal curvature variation with load',
'PEX3':'Longitudinal curvature variation with squared load',
'PEX4':'Longitudinal curvature variation with slip sign',
'PKX1':'Longitudinal slip stiffness Kx / Fz at Fznom',
'PKX2':'Longitudinal slip stiffness variation with load',
'PKX3':'Exponent in longitudinal slip stiffness with load',
'PHX1':'Horizontal shift Shx at Fznom',
'PHX2':'Horizontal shift variation with load',
'PVX1':'Vertical shift Svx / Fz at Fznom',
'PVX2':'Vertical shift variation with load',
# Aligning moment
'QBZ1':'Trail slope factor Bpt for trail at Fznom',
'QBZ2':'Trail slope variation with load',
'QBZ3':'Trail slope variation with square load',
'QBZ4':'Trail slope variation with camber',
'QBZ5':'Trail slope variation with absolute camber',
'QCZ1':'Shape factor Cpt for pneumatic trail',
'QDZ1':'Peak trail Dpt * (Fz / Fznom * R0)',
'QDZ2':'Peak trail variation with load',
'QDZ3':'Peak trail variation with camber',
'QDZ4':'Peak trail variation with square camber',
'QEZ1':'Trail curvature Ept at Fznom',
'QEZ2':'Trail curvature variation with load',
'QEZ3':'Trail curvature variation with square load',
'QEZ4':'Trail curvature variation with slip angle sign',
'QEZ5':'Trail curvature variation with camber and slip angle sign',
'QHZ1':'Horizontal shift for trail Sht at Fznom',
'QHZ2':'Horizontal shift variation with load',
'QHZ3':'Horizontal shift variation with camber',
'QHZ4':'Horizontal shift variation with camber and load',
'QBZ9':'Slope factor Br of residual torque Mzr',
'QBZ10':'Slope factor Br of residual torque Mzr',
'QDZ6':'Peak residual torque Dmr /(Fz * R0)',
'QDZ7':'Peak residual torque variation with load',
'QDZ8':'Peak residual torque variation with camber',
'QDZ9':'Peak residual torque variation with camber and load',
# Lateral combined
'RBY1':'Slope factor for combined Fy reduction',
'RBY2':'Slope variation of Fy reduction with alpha',
'RBY3':'Shift term for alpha in slope of Fy reduction',
'RCY1':'Shape factor for combined Fy reduction',
'RHY1':'Shift factor for combined Fy reduction',
'RVY1':'Slip induced side force Svyk / Muy * Fz at FZ0',
'RVY2':'Variation of Svyk / Muy * Fz with load',
'RVY3':'Variation of Svyk / Muy * Fz with camber',
'RVY4':'Variation of Svyk / Muy * Fz with slip angle',
'RVY5':'Variation of Svyk / Muy * Fz with slip',
'RVY6':'Variation of Svyk / Muy * Fz with atan(slip)',
# Longitudinal combined
'RBX1':'Slope factor of Fx reduction for combined slip',
'RBX2':'Slope variation of Fx reduction with slip',
'RCX1':'Slope factor of Fx reduction for combined slip',
'RHX1':'Shift factor of Fx reduction for combined slip',
}


def PacejkaFx(p, sigma, Fz, dFz):
    Fz0 = p['FZ0']

    # vertical shift
    Sv = Fz * (p['PVX1'] + p['PVX2'] * dFz)

    # horizontal shift
    Sh = p['PHX1'] + p['PHX2'] * dFz

    # composite slip
    S = sigma + Sh

    # slope at origin
    K = Fz * (p['PKX1'] + p['PKX2'] * dFz) * exp(-p['PKX3'] * dFz)

    # curvature factor
    E = (p['PEX1'] + p['PEX2'] * dFz + p['PEX3'] * dFz * dFz) * (1 - p['PEX4'] * copysign(1, S))

    # peak factor
    D = Fz * (p['PDX1'] + p['PDX2'] * dFz)

    # shape factor
    C = p['PCX1']

    # stiffness factor
    B =  K / (C * D)

    # force
    return D * sin(C * atan(B * S - E * (B * S - atan(B * S)))) + Sv


def PacejkaFy(p, alpha, gamma, Fz, dFz):
    Fz0 = p['FZ0']

    # vertical shift
    Sv = Fz * (p['PVY1'] + p['PVY2'] * dFz + (p['PVY3'] + p['PVY4'] * dFz) * gamma)

    # horizontal shift
    Sh = p['PHY1'] + p['PHY2'] * dFz + p['PHY3'] * gamma

    # composite slip angle
    A = alpha + Sh;

    # slope at origin
    K = p['PKY1'] * Fz0 * sin(2 * atan(Fz / (p['PKY2'] * Fz0))) * (1 - p['PKY3'] * abs(gamma))

    # curvature factor
    E = (p['PEY1'] + p['PEY2'] * dFz) * (1 - (p['PEY3'] + p['PEY4'] * gamma) * copysign(1, A))

    # peak factor
    D = Fz * (p['PDY1'] + p['PDY2'] * dFz) * (1 - p['PDY3'] * gamma * gamma)

    # shape factor
    C = p['PCY1']

    # stiffness factor
    B = K / (C * D)

    # force
    Fy = D * sin(C * atan(B * A - E * (B * A - atan(B * A)))) + Sv

    Dy = D
    BCy = B * C
    Shf = Sh + Sv / K

    return Fy, Dy, BCy, Shf


def PacejkaMz(p, alpha, gamma, Fz, dFz, Fy, BCy, Shf):
    Fz0 = p['FZ0']
    R0 = 0.3
    yz = gamma
    cosa = cos(alpha)

    Sht = p['QHZ1'] + p['QHZ2'] * dFz + (p['QHZ3'] + p['QHZ4'] * dFz) * yz

    At = alpha + Sht

    Bt = (p['QBZ1'] + p['QBZ2'] * dFz + p['QBZ3'] * dFz * dFz) * (1 + p['QBZ4'] * yz + p['QBZ5'] * abs(yz))

    Ct = p['QCZ1']

    Dt = Fz * (p['QDZ1'] + p['QDZ2'] * dFz) * (1 + p['QDZ3'] * yz + p['QDZ4'] * yz * yz) * (R0 / Fz0)

    Et = (p['QEZ1'] + p['QEZ2'] * dFz + p['QEZ3'] * dFz * dFz) * (1 + (p['QEZ4'] + p['QEZ5'] * yz) * atan(Bt * Ct * At))

    Mzt = -Fy * Dt * cos(Ct * atan(Bt * At - Et * (Bt * At - atan(Bt * At)))) * cosa

    Ar = alpha + Shf

    Br = p['QBZ10'] * BCy

    Dr = Fz * (p['QDZ6'] + p['QDZ7'] * dFz + (p['QDZ8'] + p['QDZ9'] * dFz) * yz) * R0

    Mzr = Dr * cos(atan(Br * Ar)) * cosa

    return Mzt + Mzr


def PacejkaGx(p, sigma, alpha):
    B = p['RBX1'] * cos(atan(p['RBX2'] * sigma))
    C = p['RCX1']
    Sh = p['RHX1']
    S = alpha + Sh
    G0 = cos(C * atan(B * Sh))
    G = cos(C * atan(B * S)) / G0
    return G


def PacejkaGy(p, sigma, alpha):
    B = p['RBY1'] * cos(atan(p['RBY2'] * (alpha - p['RBY3'])))
    C = p['RCY1']
    Sh = p['RHY1']
    S = sigma + Sh
    G0 = cos(C * atan(B * Sh))
    G = cos(C * atan(B * S)) / G0
    return G


def PacejkaSvy(p, sigma, alpha, gamma, dFz, Dy):
    Dv = Dy * (p['RVY1'] + p['RVY2'] * dFz + p['RVY3'] * gamma) * cos(atan(p['RVY4'] * alpha))
    Sv = Dv * sin(p['RVY5'] * atan(p['RVY6'] * sigma))
    return Sv


def PacejkadFz(p, Fz):
    Fz0 = p['FZ0']
    dFz = (Fz - Fz0) / Fz0;
    return dFz


def Pacejka(p, sigma, alpha, gamma, Fz):
    dFz = PacejkadFz(p, Fz)
    Fx = PacejkaFx(p, sigma, Fz, dFz)
    Fy, Dy, BCy, Shf = PacejkaFy(p, alpha, gamma, Fz, dFz)
    Mz = PacejkaMz(p, alpha, gamma, Fz, dFz, Fy, BCy, Shf)
    return Fx, Fy, Mz


def PacejkaCombine(p, sigma, alpha, gamma, Fx0, Fy0, Dy, dFz):
    Gx = PacejkaGx(p, sigma, alpha)
    Gy = PacejkaGy(p, sigma, alpha)
    Svy = PacejkaSvy(p, sigma, alpha, gamma, Dy, dFz)
    Fx = Gx * Fx0
    Fy = Gy * Fy0 + Svy
    return Fx, Fy

coeff_fy0 = ['a0','a1','a2','a3','a4','a5','a6','a7','a8','a9','a10','a111','a112','a12','a13']

coeff_fx0 = ['b0','b1','b2','b3','b4','b5','b6','b7','b8','b9','b10']

coeff_mz0 = ['c0','c1','c2','c3','c4','c5','c6','c7','c8','c9','c10','c11','c12','c13','c14','c15','c16','c17']


# Longitudinal force
def PacejkaFx0(p, sigma, Fz):
    # shape factor
    C = p['b0']

    # peak factor
    D = (p['b1'] * Fz + p['b2']) * Fz

    # slope at origin
    BCD = (p['b3'] * Fz + p['b4']) * Fz * exp(-p['b5'] * Fz)

    # stiffness factor
    B =  BCD / (C * D)

    # curvature factor
    E = p['b6'] * Fz * Fz + p['b7'] * Fz + p['b8']

    # curvature factor 1993
    #E = E * (1 - p['b13'] * sgn(S))

    # horizontal shift
    Sh = p['b9'] * Fz + p['b10']

    # vertical shift 1993
    #Sv = p['b11'] * Fz + p['b12']

    # composite
    S = 100 * sigma + Sh

    # longitudinal force
    return D * sin(C * atan(B * S - E * (B * S - atan(B * S))))


# Lateral force
def PacejkaFy0(p, alpha, gamma, Fz):
    # shape factor
    C = p['a0']

    # peak factor
    D = (p['a1'] * Fz + p['a2']) * Fz

    # peak factor 1993
    # D = D * (1 - p['a14'] * gamma * gamma)

    # slope at origin
    BCD = p['a3'] * sin(2.0 * atan(Fz / p['a4'])) * (1.0 - p['a5'] * fabs(gamma))

    # stiffness factor
    B = BCD / (C * D)

    # curvature factor
    E = p['a6'] * Fz + p['a7']

    # curvature factor 1993
    # E = E * (1 - (p['a15'] * gamma + p['a16']) * sgn(alpha + Sh))

    # horizontal shift
    Sh = p['a8'] * gamma + p['a9'] * Fz + p['a10']

    # horizontal shift 1993
    # Sh = p['a8'] * Fz + p['a9'] + p['a10'] * gamma

    # vertical shift
    Sv = ((p['a111'] * Fz + p['a112']) * gamma + p['a12']) * Fz + p['a13']

    # vertical shift 1993
    # Sv = p['a111'] * Fz + p['a112'] + (p['a12'] * Fz * Fz + p['a13'] * Fz) * gamma

    # composite
    S = alpha + Sh

    # lateral force
    return D * sin(C * atan(B * S - E * (B * S - atan(B * S)))) + Sv


# Aligning moment
def PacejkaMz0(p, sigma, alpha, gamma, Fz):
    # shape factor
    C = p['c0']

    # peak factor
    D = (p['c1'] * Fz + p['c2']) * Fz

    # peak factor 1993
    # D = D * (1 - p['c18'] * gamma * gamma)

    # slope at origin
    BCD = (p['c3'] * Fz + p['c4']) * Fz * (1.0 - p['c6'] * fabs(gamma)) * exp (-p['c5'] * Fz)

    # stiffness factor
    B =  BCD / (C * D)

    # curvature factor
    E = (p['c7'] * Fz * Fz + p['c8'] * Fz + p['c9']) * (1.0 - p['c10'] * fabs(gamma))

    # curvature factor 1993
    # E = (p['c7'] * Fz * Fz + p['c8'] * Fz + p['c9']) * (1.0 - (p['c19'] * gamma + p['c20']) * sgn(S)) / (1.0 - p['c10'] * fabs(gamma))

    # horizontal shift
    Sh = p['c11'] * gamma + p['c12'] * Fz + p['c13']

    # horizontal shift 1993
    # Sh = p['c11'] * Fz + p['c12'] + p['c13'] * gamma

    # vertical shift
    Sv = (p['c14'] * Fz * Fz + p['c15'] * Fz) * gamma + p['c16'] * Fz + p['c17']

    # vertical shift 1993
    # Sv = p['c14'] * Fz + p['c15'] + (p['c16'] * Fz * Fz + p['c17'] * Fz) * gamma

    # composite
    S = alpha + Sh

    # self-aligning torque
    return D * sin(C * atan(B * S - E * (B * S - atan(B * S)))) + Sv


def Pacejka0(p, sigma, alpha, gamma, Fz):
    Fx = PacejkaFx0(p, sigma, Fz)
    Fy = PacejkaFy0(p, alpha, gamma, Fz)
    Mz = PacejkaMz0(p, sigma, alpha, gamma, Fz)
    return Fx, Fy, Mz


def CosAtan(x):
    return 1.0 / sqrt(1.0 + x * x)


# Longitudinal force combining factor, alpha in rad
def PacejkaGx0(p, sigma, alpha):
    B = p['gx1'] * CosAtan(p['gx2'] * sigma)
    G = CosAtan(B * alpha)
    return G


# Lateral force combining factor, alpha in rad
def PacejkaGy0(p, sigma, alpha):
    B = p['gy1'] * CosAtan(p['gy2'] * alpha)
    G = CosAtan(B * sigma)
    return G


class ToolTip( Toplevel ):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """ 
    def __init__( self, wdgt, msg=None, msgFunc=None, delay=1, follow=True ):
        """
        Initialize the ToolTip
        
        Arguments:
          wdgt: The widget this ToolTip is assigned to
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        self.parent = self.wdgt.master                                          # The parent of the ToolTip is the parent of the ToolTips widget
        Toplevel.__init__( self, self.parent, bg='black', padx=1, pady=1 )      # Initalise the Toplevel
        self.withdraw()                                                         # Hide initially
        self.overrideredirect( True )                                           # The ToolTip Toplevel should have no frame or title bar
        
        self.msgVar = StringVar()                                               # The msgVar will contain the text displayed by the ToolTip        
        if msg == None:                                                         
            self.msgVar.set( 'No message provided' )
        else:
            self.msgVar.set( msg )
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        Message( self, textvariable=self.msgVar, bg='#FFFFDD',
                 aspect=1000 ).grid()                                           # The test of the ToolTip is displayed in a Message widget
        self.wdgt.bind( '<Enter>', self.spawn, '+' )                            # Add bindings to the widget.  This will NOT override bindings that the widget already has
        self.wdgt.bind( '<Leave>', self.hide, '+' )
        self.wdgt.bind( '<Motion>', self.move, '+' )
        
    def spawn( self, event=None ):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget
        
        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        self.after( int( self.delay * 1000 ), self.show )                       # The after function takes a time argument in miliseconds
        
    def show( self ):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()
            
    def move( self, event ):
        """
        Processes motion within the widget.
        
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        if self.follow == False:                                                # If the follow flag is not set, motion within the widget will make the ToolTip dissapear
            self.withdraw()
            self.visible = 1
        self.geometry( '+%i+%i' % ( event.x_root+10, event.y_root+10 ) )        # Offset the ToolTip 10x10 pixes southwest of the pointer
        try:
            self.msgVar.set( self.msgFunc() )                                   # Try to call the message function.  Will not change the message if the message function is None or the message function fails
        except:
            pass
        self.after( int( self.delay * 1000 ), self.show )
            
    def hide( self, event=None ):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()


# a vertical scrollable frame
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


# a base tab class
class Tab(Frame):
    def __init__(self, master, name, color):
        Frame.__init__(self, master)
        self.tab_name = name
        self.color = color

# the actual tab bar
class TabBar(Frame):
    def __init__(self, master=None, init_name=None):
        Frame.__init__(self, master)
        self.tabs = {}
        self.buttons = {}
        self.current_tab = None
        self.init_name = init_name

    def show(self):
        self.pack(side=TOP, anchor=N, fill=X)
        self.switch_tab(self.init_name or self.tabs.keys()[-1])         # switch to the first tab

    def add(self, tab):
        tab.pack_forget()                                               # hide the tab on init
        self.tabs[tab.tab_name] = tab                                   # add it to the list of tabs
        b = Button(self, text=tab.tab_name, fg=tab.color, relief=RAISED,
            command=(lambda name=tab.tab_name: self.switch_tab(name)))  # set the command to switch tabs
        b.pack(side=LEFT, fill=X, expand=YES)                           # pack the buttont to the left
        self.buttons[tab.tab_name] = b                                  # add it to the list of buttons

    def delete(self, tabname):
        if tabname == self.current_tab:
            self.current_tab = None
            self.tabs[tabname].pack_forget()
            del self.tabs[tabname]
            self.switch_tab(self.tabs.keys()[0])
        else:
            del self.tabs[tabname]
        self.buttons[tabname].pack_forget()
        del self.buttons[tabname]

    def switch_tab(self, name):
        if self.current_tab:
            self.buttons[self.current_tab].config(relief=RAISED)
            self.tabs[self.current_tab].pack_forget()           # hide the current tab
        self.tabs[name].pack(side=TOP, fill=X)                  # add the new tab to the display
        self.current_tab = name                                 # set the current tab to itself
        self.buttons[name].config(relief=FLAT)                  # set it to the selected style


# custom slider class
class Slider(Frame):
    def __init__(self, parent, text, v, vmin, vmax, call):
        Frame.__init__(self, parent)
        self.call = call
        self.v = StringVar()
        self.tl = Label(self, text=text)
        self.tl.pack(side=LEFT, anchor=S)
        self.s = Scale(self, from_=vmin, to=vmax, resolution=(vmax-vmin)/10000.0,
                           length=160, orient="horizontal", showvalue=0, command=self.command)
        self.s.pack(side=RIGHT, anchor=S)
        self.vl = Label(self, textvariable=self.v)
        self.vl.pack(side=RIGHT, anchor=S)
        self.set(v)

    def command(self, event):
        self.v.set(str(event))
        self.call(event)

    def get(self):
        return self.s.get()

    def set(self, v):
        self.v.set(str(v))
        self.s.set(v)


def addSlider(parent, txt, val, vmin, vmax, vinfo, call):
    s = Slider(parent, txt, val, vmin, vmax, call)
    s.pack(anchor=N, fill=X)
    ToolTip(s.tl, msg=vinfo, delay=0.3)
    return s


class App:
    def __init__(self, root):
        self.need_redraw = False
        self.samples = 512
        self.slip_angle_scale = (60.0 / 180.0 * pi) / self.samples
        self.slip_scale = 2.0 / self.samples
        self.coeff = coeff_default.copy()
        self.coeff0 = {}
        self.file_opt = {
            'defaultextension':'.tiren',
            'filetypes':[('tire files', '.tiren'), ('all files', '.*')],
            'initialdir':'C:\\',
            'initialfile':'touring.tiren',
            'parent':root,
            'title':'Select tire config file',
        }
        self.file_opt_ref = {
            'defaultextension':'.tire',
            'filetypes':[('tire files', '.tire'), ('all files', '.*')],
            'initialdir':'C:\\',
            'initialfile':'touring.tire',
            'parent':root,
            'title':'Select tire config file',
        }

        root.title('VDrift Tire Editor NO')

        frame = VerticalScrolledFrame(root)
        frame.pack(fill=BOTH, expand=TRUE)

        sframe = Frame(frame.interior, width=256)
        sframe.pack(side=LEFT, fill=Y)
        cframe = Frame(frame.interior, width=512)
        cframe.pack(side=TOP, anchor=NW)

        self.canvas = Canvas(cframe, width=512, height=512)
        self.canvas.pack(fill=BOTH, expand=YES)

        # load/save buttons
        bframe = Frame(sframe, width=256)
        Button(bframe, text='Load Ref Old', command=self.loadref).pack(side=LEFT, fill=X, expand=YES)
        Button(bframe, text='Load', command=self.load).pack(side=LEFT, fill=X, expand=YES)
        Button(bframe, text='Save', command=self.save).pack(side=LEFT, fill=X, expand=YES)
        bframe.pack(anchor=N, fill=X)

        # base coeff sliders
        self.sliders = {}
        for n in coeff_base:
            s = addSlider(sframe, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        # tire coeff slider tabs
        bar = TabBar(sframe, 'Fx')
        tabx = Tab(sframe, 'Fx', 'red')
        taby = Tab(sframe, 'Fy', 'blue')
        tabz = Tab(sframe, 'Mz', 'brown')
        tabc = Tab(sframe, 'Fxy', 'black')

        for n in coeff_fx:
            s = addSlider(tabx, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        for n in coeff_fy:
            s = addSlider(taby, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        for n in coeff_mz:
            s = addSlider(tabz, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        for n in coeff_fxy:
            s = addSlider(tabc, n, self.coeff[n], coeff_min[n], coeff_max[n], coeff_info[n], self.update)
            self.sliders[n] = s

        bar.add(tabx)
        bar.add(taby)
        bar.add(tabz)
        bar.add(tabc)
        bar.show()

        self.update('')

    def loadref(self):
        f = filedialog.askopenfile(mode='r', **self.file_opt_ref)
        if not f: return
        for line in f:
            line = line.split('#')[0]
            if line.startswith('a') or line.startswith('b') or line.startswith('c') or line.startswith('g'):
                name, value = line.split('=')
                name, value = name.strip(), value.strip()
                self.coeff0[name] = float(value)
        self.updateCanvas()

    def load(self):
        f = filedialog.askopenfile(mode='r', **self.file_opt)
        if f:
            self.readCoeff(f)

    def save(self):
        f = filedialog.asksaveasfile(mode='w', **self.file_opt)
        if f:
            self.writeCoeff(f)

    def readCoeff(self, f):
        for line in f:
            if line.startswith('F') or line.startswith('P') or line.startswith('Q') or line.startswith('R'):
                name, value = line.split('=')
                name, value = name.strip(), value.strip()
                self.coeff[name] = float(value)
                self.sliders[name].set(float(value))
        self.updateCanvas()

    def writeCoeff(self, f):
        f.write('restitution = 0.1\n')
        f.write('tread = 0.25\n')
        f.write('rolling-resistance = 1.3e-2, 6.5e-6\n')
        f.write('{0}={1:f}\n'.format('FZ0', self.coeff['FZ0']))
        f.write('# Lateral force\n')
        for n in coeff_fy:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))
        f.write('# Longitudinal force\n')
        for n in coeff_fx:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))
        f.write('# Aligning moment\n')
        for n in coeff_mz:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))
        f.write('# Lateral/longitudinal combined\n')
        for n in coeff_fxy:
            f.write('{0}={1:f}\n'.format(n, self.coeff[n]))

    def sampleData(self, coeff):
        fz = self.coeff['fz']
        camber = self.coeff['camber'] / 180.0 * pi
        slip_angle = self.coeff['aos'] / 180.0 * pi
        samples = self.samples
        samples2 = self.samples / 2
        # force, torque curves
        afx, afy, amz = [], [], []
        for i in range(0, samples, 1):
            s = self.slip_scale * (i - samples2)
            a = self.slip_angle_scale * (i - samples2)
            fx, fy, mz = Pacejka(coeff, s, a, camber, fz)
            afx.append((i, samples2 * (1 - 0.5 * fx / fz)))
            afy.append((i, samples2 * (1 + 0.5 * fy / fz)))
            amz.append((i, samples2 * (1 +  10 * mz / fz)))
        # combined force curve
        dfz = PacejkadFz(coeff, fz)
        fy, dy, bcy, shf = PacejkaFy(coeff, slip_angle, camber, fz, dfz)
        atcp = []
        for i in range(0, samples, 1):
            s = self.slip_scale * (i - samples2)
            fx = 2 * fz * (1 - afx[i][1] / samples2)
            fcx, fcy = PacejkaCombine(coeff, s, slip_angle, camber, fx, fy, dy, dfz)
            atcp.append((samples2 * (1 - 0.5 * fcx / fz), samples2 * (1 - 0.5 * fcy / fz)))
        fy, dy, bcy, shf = PacejkaFy(coeff, -slip_angle, camber, fz, dfz)
        atcn = []
        for i in range(0, samples, 1):
            s = self.slip_scale * (i - samples2)
            fx = 2 * fz * (1 - afx[samples - 1 - i][1] / samples2)
            fcx, fcy = PacejkaCombine(coeff, s, -slip_angle, camber, fx, fy, dy, dfz)
            atcn.append((samples2 * (1 - 0.5 * fcx / fz), samples2 * (1 - 0.5 * fcy / fz)))
        return afx, afy, amz, atcp, atcn

    def sampleData0(self, coeff):
        camber = self.coeff['camber']
        fz = self.coeff['fz'] * 0.001
        sa = self.coeff['aos'] / 180.0 * pi
        fyp = PacejkaFy0(coeff, sa / pi * 180.0, camber, fz)
        fyn = PacejkaFy0(coeff, -sa / pi * 180.0, camber, fz)
        samples = self.samples
        samples2 = self.samples / 2
        slip_angle_scale = self.slip_angle_scale / pi * 180
        afx, afy, amz, acp, acn = [], [], [], [], []
        for i in range(0, samples, 1):
            s = self.slip_scale * (i - samples2)
            a = slip_angle_scale * (i - samples2)
            fx, fy, mz = Pacejka0(coeff, s, a, camber, fz)
            gx = PacejkaGx0(coeff, s, sa)
            gy = PacejkaGy0(coeff, s, sa)
            mux = gx * fx / fz
            muyp = gy * fyp / fz
            muyn = gy * fyn / fz
            afx.append((i, samples2 * (1 - 0.0005 * fx / fz)))
            afy.append((i, samples2 * (1 - 0.0005 * fy / fz)))
            amz.append((i, samples2 * (1 - 0.0100 * mz / fz)))
            acp.append((samples2 * (1 - 0.0005 * mux), samples2 * (1 - 0.0005 * muyp)))
            acn.append((samples2 * (1 - 0.0005 * mux), samples2 * (1 - 0.0005 * muyn)))
        return afx, afy, amz, acp, acn

    def updateCanvas(self):
        # clear canvas
        s = self.samples
        self.canvas.delete(ALL)
        self.canvas.create_line(s/4, 2, s/4, s, width=1, fill="grey")
        self.canvas.create_line(s/2, 2, s/2, s, width=1, fill="black")
        self.canvas.create_line(3*s/4, 2, 3*s/4, s, width=1, fill="grey")
        self.canvas.create_line(2, s/4, s, s/4, width=1, fill="grey")
        self.canvas.create_line(2, s/2, s, s/2, width=1, fill="black")
        self.canvas.create_line(2, 3*s/4, s, 3*s/4, width=1, fill="grey")
        # draw ref curves
        if self.coeff0:
            fx, fy, mz, cp, cn = self.sampleData0(self.coeff0)
            self.canvas.create_line(fx, width=1, fill="light pink")
            self.canvas.create_line(fy, width=1, fill="light blue")
            self.canvas.create_line(mz, width=1, fill="sandy brown")
            self.canvas.create_line(cp, width=1, fill="dark grey")
            self.canvas.create_line(cn, width=1, fill="dark grey")
        # draw curves
        fx, fy, mz, tcp, tcn = self.sampleData(self.coeff)
        self.canvas.create_line(fx, width=1, fill="red")
        self.canvas.create_line(fy, width=1, fill="blue")
        self.canvas.create_line(mz, width=1, fill="brown")
        self.canvas.create_line(tcp, width=1, fill="black")
        self.canvas.create_line(tcn, width=1, fill="black")
        self.need_redraw = False

    def update(self, event):
        need_redraw = False
        for n, s in self.sliders.items():
            need_redraw = need_redraw | (self.coeff[n] != s.get())
            self.coeff[n] = s.get()
        if not self.need_redraw and need_redraw:
            self.need_redraw = need_redraw
            self.canvas.after_idle(self.updateCanvas)

    def resize(event):
        #todo: event.width, event.height
        canvas.bind("<Configure>", resize)


tk = Tk()
app = App(tk)
tk.mainloop()
