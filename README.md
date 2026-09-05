# `roman_mond` – Flexible Dynamics Toolkit for Galaxy Data

A clean, notebook-friendly Python library for testing alternative gravity and dynamics models against galaxy and cluster rotation-curve data. Designed to work with Roman-style catalogs and similar surveys, with a focus on rapid experimentation, clear plots, and easy model swapping.

***

## What It Does

- **Plug-and-play dynamics models**  
  Swap between Newtonian, MOND-like, and custom acceleration laws with a single argument. Built to make it easy to prototype “what if?” theories without rewriting your analysis pipeline.

- **Rotation-curve fitting**  
  Fit observed \(v(r)\) data with different dynamical prescriptions, including optional environmental corrections.

- **Kaggle-style workflow**  
  Minimal setup, vectorized numerics, and ready-to-use plotting functions so you can go from CSV to figures in a few cells.

- **Extensible by design**  
  Add new interpolation functions, acceleration laws, or environmental terms as small, isolated modules.

***

## Installation

```bash
git clone https://github.com/yourusername/roman_mond.git
cd roman_mond
pip install -r requirements.txt
```

### `requirements.txt`

```text
numpy>=1.24
scipy>=1.11
pandas>=2.0
matplotlib>=3.7
astropy>=5.3
```

Usage in a notebook:

```python
import roman_mond as rm
```

***

## Quick Start

```python
import roman_mond as rm

# Load and preprocess a galaxy catalog
df = rm.load_roman_catalog("galaxies.csv")
galaxies = rm.preprocess_roman_data(df)

# Pick one galaxy
gid = list(galaxies.keys())[0]
g = galaxies[gid]

r = g["r"]
v_obs = g["v_obs"]
v_err = g["v_err"]
M_star = g["M_star"]
M_gas = g["M_gas"]

# Try a MOND-like model
v_model = rm.model_v_mond(r, M_star, M_gas, a_ext=0.0, mu_func_name="simple")

# Optionally fit a simple halo-based model
popt, _ = rm.fit_lcdm_rotation_curve(r, v_obs, v_err, M_star, M_gas)
M_halo_fit = popt[0]
v_halo = rm.model_v_lcdm(r, M_star, M_gas, M_halo_fit)

# Plot
rm.plot_rotation_curves(r, v_obs, v_err, v_model, v_halo,
                        galaxy_id=gid, save_path="rc_fit.png")
```

***

## Core Ideas

The library is built around a few simple abstractions:

- **Acceleration laws**  
  Functions that map baryonic mass profiles and radii to predicted accelerations or velocities.

- **Interpolation / transition functions**  
  Control how the dynamics change between high- and low-acceleration regimes.

- **Environmental terms**  
  Optional corrections that mimic external-field-like effects or other large-scale influences.

You can treat the built-in MOND-like models as just one point in a larger space of possible theories. The API is intentionally generic so you can:

- Define new transition functions  
- Modify the effective acceleration scale  
- Add extra terms that depend on environment, radius, or mass  

All while reusing the same data loading, fitting, and plotting code.

***

## Library Structure

```text
roman_mond/
├─ __init__.py
├─ data.py          # Catalog loading and preprocessing
├─ mond.py          # Core acceleration laws and transition functions
├─ efe.py           # Environmental / external-field-like corrections
├─ fit.py           # Fitting utilities for different models
├─ plot.py          # Rotation-curve and residual plots
├─ utils.py         # Constants, units, helpers
└─ examples/
   └─ demo_notebook.ipynb
```

### Key Functions

**Data**

- `load_roman_catalog(path, filetype="csv")`
- `preprocess_roman_data(df)`

**Dynamics**

- `interpolation_functions()` → built-in transition functions  
- `mond_acceleration(aN, mu_func, a0_val)`  
- `newtonian_acceleration(M, r)`  

**Environmental Corrections**

- `effective_a0(a_ext, a0_val, mu_func_name)`  
- `efe_correction(aN, a_ext, mu_func_name, a0_val)`  

**Fitting**

- `model_v_mond(r, M_star, M_gas, a_ext, mu_func_name, a0_val)`  
- `model_v_lcdm(r, M_star, M_gas, M_halo, c_halo)`  
- `fit_mond_rotation_curve(...)`  
- `fit_lcdm_rotation_curve(...)`  

**Plotting**

- `plot_rotation_curves(...)`  
- `plot_residuals(...)`  

***

## Adapting to Your Data

To use this with your own catalogs:

1. Put your data in a CSV or Parquet file with columns like:
   - Galaxy ID
   - Radius
   - Rotation velocity and error
   - Stellar and gas mass (or proxies)

2. Adjust the column mapping in `data.py` to match your schema.

3. Use `preprocess_roman_data` to get a dictionary of galaxies, then plug into the modeling and fitting functions.

You can easily add new loaders for lensing data, velocity dispersion profiles, or simulated catalogs without touching the rest of the code.

***

## Example Notebook

`examples/demo_notebook.ipynb` shows:

- Loading a mock catalog  
- Comparing different transition functions  
- Fitting multiple galaxies in a loop  
- Stacking residuals by mass or environment  
- Saving clean figures for reports or posts  

***

## License

MIT License – see `LICENSE`.

***

## Contributing

Contributions are welcome, especially:

- New acceleration laws or transition functions  
- More realistic halo or environment models  
- Readers for specific survey formats or simulations  
- Utilities for batch fitting and model comparison  

Open issues or pull requests on GitHub to extend the toolkit.
