# roman_mond/mond.py

import numpy as np
from .utils import a0

def interpolation_functions():
    """
    Return a dict of common MOND interpolation functions.
    
    Each function takes x = a/a0 and returns mu(x).
    """
    def mu_standard(x):
        # Standard: mu = x / sqrt(1 + x^2)
        return x / np.sqrt(1 + x**2)

    def mu_simple(x):
        # Simple: mu = x / (1 + x)
        return x / (1 + x + 1e-30)

    def mu_ravier(x):
        # Ravier-type (example): mu = x / (1 + x**n)^(1/n), n=2
        n = 2.0
        return x / (1 + x**n)**(1/n)

    return {
        "standard": mu_standard,
        "simple": mu_simple,
        "ravier": mu_ravier,
    }

def newtonian_acceleration(M, r):
    """
    Newtonian acceleration from mass M (M_sun) at radius r (kpc).
    Returns a_N in (km/s)^2 / kpc.
    """
    G = 4.30091e-6  # (km/s)^2 kpc / M_sun
    return G * M / (r**2 + 1e-30)

def mond_acceleration(aN, mu_func, a0_val=a0):
    """
    Solve MOND equation: mu(a/a0) * a = aN
    
    Given Newtonian acceleration aN and interpolation function mu,
    return MOND acceleration a (same units as aN and a0).
    
    Uses numerical root-finding per element.
    """
    from scipy.optimize import brentq

    aN = np.asarray(aN, dtype=float)
    a = np.empty_like(aN)

    def monda_eq(a_trial, aN_val):
        x = a_trial / a0_val
        mu = mu_func(x)
        return mu * a_trial - aN_val

    for i, aN_val in enumerate(aN):
        if aN_val <= 0:
            a[i] = 0.0
            continue
        # Bracket: a in [aN, max(aN, a0*10)]
        a_low = aN_val
        a_high = max(aN_val, a0_val * 10.0)
        try:
            a[i] = brentq(monda_eq, a_low, a_high, args=(aN_val,))
        except ValueError:
            # Fallback: approximate deep-MOND limit a ≈ sqrt(aN * a0)
            a[i] = np.sqrt(aN_val * a0_val)

    return a
