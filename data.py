# roman_mond/data.py

import pandas as pd
import numpy as np
from astropy import units as u

def load_roman_catalog(path, filetype="csv"):
    """
    Load a Roman-style galaxy/cluster catalog.
    
    Expected columns (example):
      - galaxy_id
      - radius_kpc
      - v_rot_km_s
      - v_rot_err_km_s
      - stellar_mass_sol
      - gas_mass_sol
      - distance_mpc
      - incl_deg
    """
    if filetype == "csv":
        df = pd.read_csv(path)
    elif filetype == "parquet":
        df = pd.read_parquet(path)
    else:
        raise ValueError("filetype must be 'csv' or 'parquet'")
    return df

def preprocess_roman_data(df):
    """
    Preprocess Roman catalog for MOND analysis.
    
    Returns a dict per galaxy with:
      - r: radius (kpc)
      - v_obs: observed rotation velocity (km/s)
      - v_err: error on v_obs
      - M_star: stellar mass (M_sun)
      - M_gas: gas mass (M_sun)
    """
    # Example mapping; adjust to your real Roman schema
    df = df.copy()
    
    # Ensure positive radii and velocities
    df = df[df["radius_kpc"] > 0].copy()
    df = df[df["v_rot_km_s"] > 0].copy()
    
    # Group by galaxy_id
    galaxies = {}
    for gid, sub in df.groupby("galaxy_id"):
        galaxies[gid] = {
            "r": sub["radius_kpc"].values,
            "v_obs": sub["v_rot_km_s"].values,
            "v_err": sub["v_rot_err_km_s"].values,
            "M_star": sub["stellar_mass_sol"].mean(),
            "M_gas": sub["gas_mass_sol"].mean(),
        }
    return galaxies
