import numpy as np
import xarray as xr  # Preferred scientific package for handling netCDF climate cubes

def step_rk4_lagrangian_drift(lat, lon, dt, alpha, netcdf_filepath):
    """
    Vectorized 4th-Order Runge-Kutta Solver parsing physical 
    oceanic NetCDF surface wind vectors and hydro-current matrices.
    """
    # Open the historical environmental reanalysis cube (GLORYS / ERA5)
    # Essential: file must contain time matching March-June 2014 variables
    ds = xr.open_dataset(netcdf_filepath)
    
    def get_velocity_field(current_lat, current_lon):
        # Query nearest coordinate grid node inside the historical data structure
        node_data = ds.sel(latitude=current_lat, longitude=current_lon, method="nearest")
        
        # Pull authentic surface currents (u=zonal, v=meridional)
        u_current = float(node_data['uo'].values)  # Marine current eastward velocity
        v_current = float(node_data['vo'].values)  # Marine current northward velocity
        
        # Pull authentic surface wind components 
        u_wind = float(node_data['u10'].values)    # 10m wind vector eastward component
        v_wind = float(node_data['v10'].values)    # 10m wind vector northward component
        
        # Combine forces applying your structural aerodynamic leeway factor (alpha)
        u_final = u_current + (alpha * u_wind)
        v_final = v_current + (alpha * v_wind)
        return u_final, v_final

    R_E = 111000.0  # Meters per degree mapping scale
    
    # --- Execute RK4 Mathematical Sub-Steps ---
    u1, v1 = get_velocity_field(lat, lon)
    k1_lat = (v1 * dt) / R_E
    k1_lon = (u1 * dt) / (R_E * math.cos(math.radians(lat)))
    
    u2, v2 = get_velocity_field(lat + k1_lat/2, lon + k1_lon/2)
    k2_lat = (v2 * dt) / R_E
    k2_lon = (u2 * dt) / (R_E * math.cos(math.radians(lat + k1_lat/2)))
    
    u3, v3 = get_velocity_field(lat + k2_lat/2, lon + k2_lon/2)
    k3_lat = (v3 * dt) / R_E
    k3_lon = (u3 * dt) / (R_E * math.cos(math.radians(lat + k2_lat/2)))
    
    u4, v4 = get_velocity_field(lat + k3_lat, lon + k3_lon)
    k4_lat = (v4 * dt) / R_E
    k4_lon = (u4 * dt) / (R_E * math.cos(math.radians(lat + k3_lat)))
    
    # Final positional translation update vector
    new_lat = lat + (k1_lat + 2*k2_lat + 2*k3_lat + k4_lat) / 6.0
    new_lon = lon + (k1_lon + 2*k2_lon + 2*k3_lon + k4_lon) / 6.0
    
    # Inject sub-grid stochastic diffusion perturbations to simulate turbulent ocean mixing
    new_lat += np.random.normal(0, 0.0024) 
    new_lon += np.random.normal(0, 0.0028)
    
    return new_lat, new_lon

