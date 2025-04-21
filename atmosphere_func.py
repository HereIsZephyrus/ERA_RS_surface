import math
from constants import atmosphere_constants as constants
import logging

logger = logging.getLogger("atmosphere")

def rho(p, Ta):
    logger.debug(f"Calculating density of air at {p} Pa and {Ta} K")
    return p / (constants['R'] * Ta)

def u_star(u):
    logger.debug(f"Calculating friction velocity at {u} m/s")
    return 0.03 * u

def es(Ts):
    logger.debug(f"Calculating saturation vapor pressure at {Ts} K")
    return 0.6108 * math.exp(17.27 * Ts / (Ts + 237.3))

def ea(Td):
    logger.debug(f"Calculating actual vapor pressure at {Td} K")
    return 0.6108 * math.exp(17.27 * Td / (Td + 237.3))

def rs(NDVI):
    logger.debug(f"Calculating surface resistance at {NDVI}")
    return 100 / (NDVI + 0.1)

def dT(Ta, Ts):
    logger.debug(f"Calculating temperature difference at {Ta} K and {Ts} K")
    return Ta - Ts

def Qh(rho, Cp, dT, ra):
    logger.debug(f"Calculating sensible heat flux at {rho} kg/m^3, {Cp} J/(kg*K), {dT} K, {ra} m")
    return rho * Cp * dT / ra

def Qe(rho, es, ea, ra, rs):
    logger.debug(f"Calculating latent heat flux at {rho} kg/m^3, {es} Pa, {ea} Pa, {ra} m, {rs}")
    return rho * constants['Cp'] * (es - ea) / (constants['lambda'] * (ra + rs))

def ra(u_star):
    z2 = 2
    z1 = 0.1
    logger.debug(f"Calculating aerodynamic resistance at {u_star} m/s")
    return math.log(z2 / z1) / (constants['von_karman'] * u_star)

