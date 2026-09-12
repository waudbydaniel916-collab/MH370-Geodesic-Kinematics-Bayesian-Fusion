import math
import numpy as np
import xarray as xr
import os

def step_rk4_lagrangian_drift(lat, lon, current_time_str, dt, alpha, netcdf_filepath):
    """
    Vectorized 4th-Order Runge-Kutta Solver parsing physical 
    oceanic NetCDF surface wind vectors and hydro-current matrices with explicit time-tracking.
    """
    # Open the dataset globally
    ds = xr.open_dataset(netcdf_filepath)
    
    def get_velocity_field(target_lat, target_lon):
        # Explicitly query using the current temporal slice alongside spatial nodes
        node_data = ds.sel(time=current_time_str, latitude=target_lat, longitude=target_lon, method="nearest")
        
        # FIXED: Updated variable names to match your specific NetCDF file schema
        u_current = float(node_data['u_current'].values)
        v_current = float(node_data['v_current'].values)
        u_wind = float(node_data['u_wind'].values)
        v_wind = float(node_data['v_wind'].values)
        
        u_final = u_current + (alpha * u_wind)
        v_final = v_current + (alpha * v_wind)
        return u_final, v_final

    R_E = 111000.0
    
    # Step 1
    u1, v1 = get_velocity_field(lat, lon)
    k1_lat = (v1 * dt) / R_E
    k1_lon = (u1 * dt) / (R_E * math.cos(math.radians(lat)))
    
    # Step 2
    u2, v2 = get_velocity_field(lat + k1_lat/2, lon + k1_lon/2)
    k2_lat = (v2 * dt) / R_E
    k2_lon = (u2 * dt) / (R_E * math.cos(math.radians(lat + k1_lat/2)))
    
    # Step 3
    u3, v3 = get_velocity_field(lat + k2_lat/2, lon + k2_lon/2)
    k3_lat = (v3 * dt) / R_E
    k3_lon = (u3 * dt) / (R_E * math.cos(math.radians(lat + k2_lat/2)))
    
    # Step 4
    u4, v4 = get_velocity_field(lat + k3_lat, lon + k3_lon)
    k4_lat = (v4 * dt) / R_E
    k4_lon = (u4 * dt) / (R_E * math.cos(math.radians(lat + k3_lat)))
    
    new_lat = lat + (k1_lat + 2*k2_lat + 2*k3_lat + k4_lat) / 6.0
    new_lon = lon + (k1_lon + 2*k2_lon + 2*k3_lon + k4_lon) / 6.0
    
    # Stochastic dispersion
    new_lat += np.random.normal(0, 0.0024)
    new_lon += np.random.normal(0, 0.0028)
    
    return new_lat, new_lon

# ==========================================
# FILE EXECUTION DRIVER 
# ==========================================
if __name__ == "__main__":
    test_lat = -32.9530
    test_lon = 92.9866
    test_time = "2014-03-08T00:00:00"  
    test_dt = 3600                     # 1 hour step
    test_alpha = 0.03                  # 3% leeway factor
    
    # Point directly to your local file in the repo
    dummy_nc_path = "historical_hindcast.nc" 

    print(f"  Initialising Lagrangian RK4 test step for timeline: {test_time}")
    print(f"  Starting position: {test_lat:.4f}°S, {test_lon:.4f}°E")

    if not os.path.exists(dummy_nc_path):
        print(f"\n  Error: Cannot find your environmental matrix data file at: '{dummy_nc_path}'")
    else:
        try:
            next_lat, next_lon = step_rk4_lagrangian_drift(
                lat=test_lat, 
                lon=test_lon, 
                current_time_str=test_time, 
                dt=test_dt, 
                alpha=test_alpha, 
                netcdf_filepath=dummy_nc_path
            )
            print("\n  RK4 Step Completed Successfully!")
            print(f"  New projected coordinates: {next_lat:.4f}°S, {next_lon:.4f}°E")
            
        except Exception as e:
            print(f"\n  Execution stopped due to data extraction error: {e}")



