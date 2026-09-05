# roman_mond/efe.py

import numpy as np
from .utils import a0
from .mond import interpolation_functions, newtonian_acceleration

def effective_a0(a_ext, a0_val=a0, mu_func_name="simple"):
    """
    Compute an effective a0 in the presence of an external field a_ext.
    
    Approximation: a0_eff = a0 / nu(a_ext/a0), where nu = 1/mu.
    Uses the chosen interpolation function.
    """
    mu_funcs = interpolation_functions()
    mu_func = mu_funcs[mu_func_name]
    
    x = a_ext / a0_val
    mu = mu_func(x)
    nu = 1.0 / (mu + 1e-30)
    return a0_val / nu

def efe_correction(aN, a_ext, mu_func_name="simple", a0_val=a0):
    """
    Approximate MOND acceleration with External Field Effect.
    
    Strategy:
      - Compute effective a0 under external field a_ext.
      - Solve MOND equation with a0_eff instead of a0.
    
    Returns a_MOND_EFE.
    """
    from .mond import mond_acceleration
    
    a0_eff = effective_a0(a_ext, a0_val, mu_func_name)
    
    # Reuse mond_acceleration but with scaled a0
    def mond_accel_with_a0(aN_local, a0_local):
        mu_funcs = interpolation_functions()
        mu_func = mu_funcs[mu_func_name]
        
        from scipy.optimize import brentq
        aN_local = np.asarray(aN_local, dtype=float)
        a = np.empty_like(aN_local)

        def monda_eq(a_trial, aN_val):
            x = a_trial / a0_local
            mu = mu_func(x)
            return mu * a_trial - aN_val

        for i, aN_val in enumerate(aN_local):
            if aN_val <= 0:
                a[i] = 0.0
                continue
            a_low = aN_val
            a_high = max(aN_val, a0_local * 10.0)
            try:
                a[i] = brentq(monda_eq, a_low, a_high, args=(aN_val,))
            except ValueError:
                a[i] = np.sqrt(aN_val * a0_local)
        return a

    return mond_accel_with_a0(aN, a0_eff)
