# roman_mond/utils.py

import numpy as np
from astropy import units as u
from astropy.constants import G

# MOND acceleration scale
a0_val = 1.2e-10 * u.m / u.s**2
a0 = a0_val.to(u.km / u.s**2 / u.kpc).value  # ~ 3700 (km/s)^2/kpc

def to_si(value, unit):
    """Convert astropy Quantity to SI value (float)."""
    return value.to(u.Unit(unit)).value

def safe_divide(num, den, fill=0.0):
    """Safe division avoiding divide-by-zero."""
    return np.where(den == 0, fill, num / den)
