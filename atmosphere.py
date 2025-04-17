import math

constants = {
    'Cp': 1004,
    'von_karman': 0.4,
    'g': 9.81,
    'lambda': 0.66,
    'R': 287
}

def rho(p, Ta):
    return p / (constants['R'] * Ta)

def u_star(u):
    return 0.03 * u

def es(Ts):
    return 0.6108 * math.exp(17.27 * Ts / (Ts + 237.3))

def ea(Td):
    return 0.6108 * math.exp(17.27 * Td / (Td + 237.3))

def rs(NDVI):
    return 100 / (NDVI + 0.1)

def dT(Ta, Ts):
    return Ta - Ts

def Qh(rho, Cp, dT, ra):
    return rho * Cp * dT / ra

def Qe(rho, es, ea, ra, rs):
    return rho * constants['Cp'] * (es - ea) / (constants['lambda'] * (ra + rs))

def ra(u_star):
    z2 = 2
    z1 = 0.1
    return math.log(z2 / z1) / (constants['von_karman'] * u_star)

