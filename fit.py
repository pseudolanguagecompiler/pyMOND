# roman_mond/fit.py

import numpy as np
from scipy.optimize import curve_fit
from .mond import newtonian_acceleration, mond_acceleration, interpolation_functions
from .efe import efe_correction

def model_v_mond(r, M_star, M_gas, a_ext=0.0, mu_func_name="simple", a0_val=None):
    """
    MOND model for rotation curve v(r).
    
    Parameters:
      - r: radius (kpc)
      - M_star, M_gas: masses in M_sun
      - a_ext: external field (km/s^2/kpc)
      - mu_func_name: interpolation function name
      - a0_val: if None, uses default a0
    
    Returns v_pred (km/s).
    """
    from .utils import a0 as a0_default
    if a0_val is None:
        a0_val = a0_default

    mu_funcs = interpolation_functions()
    mu_func = mu_funcs[mu_func_name]

    M_tot = M_star + M_gas
    aN = newtonian_acceleration(M_tot, r)

    if a_ext > 0:
        aM = efe_correction(aN, a_ext, mu_func_name, a0_val)
    else:
        aM = mond_acceleration(aN, mu_func, a0_val)

    v_pred = np.sqrt(aM * r + 1e-30)
    return v_pred

def model_v_lcdm(r, M_star, M_gas, M_halo, c_halo=10.0):
    """
    Simple ΛCDM model: stellar + gas + NFW halo.
    
    Very simplified: treat halo as contributing a flat asymptotic velocity.
    For serious work, replace with full NFW profile.
    """
    G = 4.30091e-6  # (km/s)^2 kpc / M_sun
    M_b = M_star + M_gas
    
    a_b = G * M_b / (r**2 + 1e-30)
    # Simplified halo: constant circular velocity contribution
    v_halo = 150.0 * np.sqrt(M_halo / 1e12)  # rough scaling
    a_h = v_halo**2 / (r + 1e-30)
    
    a_tot = a_b + a_h
    v_pred = np.sqrt(a_tot * r + 1e-30)
    return v_pred

def fit_mond_rotation_curve(r, v_obs, v_err, M_star, M_gas, a_ext=0.0, mu_func_name="simple"):
    """
    Fit MOND model to a single galaxy rotation curve.
    
    Free parameters: M_star, M_gas (optionally a_ext).
    Here we fix M_star, M_gas from data and fit only a scaling factor.
    """
    from .utils import a0 as a0_default

    def model_scaled(r, f_star, f_gas):
        M_star_eff = f_star * M_star
        M_gas_eff = f_gas * M_gas
        return model_v_mond(r, M_star_eff, M_gas_eff, a_ext, mu_func_name)

    p0 = [1.0, 1.0]
    bounds = ([0.1, 0.1], [5.0, 5.0])

    popt, pcov = curve_fit(model_scaled, r, v_obs, sigma=v_err, absolute_sigma=True,
                           p0=p0, bounds=bounds, maxfev=5000)
    return popt, pcov

def fit_lcdm_rotation_curve(r, v_obs, v_err, M_star, M_gas):
    """
    Fit simple ΛCDM model to a single galaxy rotation curve.
    
    Free parameters: M_halo (and optionally c_halo).
    """
    def model_scaled(r, M_halo):
        return model_v_lcdm(r, M_star, M_gas, M_halo)

    p0 = [1e12]
    bounds = ([1e10], [1e14])

    popt, pcov = curve_fit(model_scaled, r, v_obs, sigma=v_err, absolute_sigma=True,
                           p0=p0, bounds=bounds, maxfev=5000)
    return popt, pcov
