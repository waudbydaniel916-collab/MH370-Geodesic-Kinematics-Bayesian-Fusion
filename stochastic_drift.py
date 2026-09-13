import math
import numpy as np
import xarray as xr
import os

def step_rk4_multi_leeway_drift(lat, lon, current_time_str, dt, leeway_class, wind_nc_path):
    """
    Vectorised 4th-Order Runge-Kutta Solver parsing authentic atmospheric 
    ECMWF ERA5 matrices using dynamic debris-specific aerodynamic leeway profiles.
    """
    ds_wind = xr.open_dataset(wind_nc_path)
    
    # Define empirical leeway coefficients mapping to distinct real-world debris types
    leeway_profiles = {
        "low_windage": 0.01,    # Dense fragments, engine cowlings, structural framing
        "mid_windage": 0.03,    # Standard interior composite panels, luggage fragments
        "high_windage": 0.05    # High-buoyancy hollow components (e.g., the Réunion Flaperon)
    }
    
    # Retrieve the target coefficient or fallback to standard 3% profile
    alpha = leeway_profiles.get(leeway_class, 0.03)
    
    def get_velocity_field(target_lat, target_lon):
        wind_node = ds_wind.sel(valid_time=current_time_str, latitude=target_lat, longitude=target_lon, method="nearest")
        
        u_wind = float(wind_node['u10'].values)
        v_wind = float(wind_node['v10'].values)
        
        # Subtropical gyre current baseline vector mapping
        u_current = 0.05 + (target_lat * 0.001)
        v_current = -0.02
        
        u_final = u_current + (alpha * u_wind)
        v_final = v_current + (alpha * v_wind)
        return u_final, v_final

    R_E = 111000.0  
    
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
    
    new_lat = lat + (k1_lat + 2*k2_lat + 2*k3_lat + k4_lat) / 6.0
    new_lon = lon + (k1_lon + 2*k2_lon + 2*k3_lon + k4_lon) / 6.0
    
    new_lat += np.random.normal(0, 0.0024)
    new_lon += np.random.normal(0, 0.0028)
    
    return new_lat, new_lon

if __name__ == "__main__":
    test_lat, test_lon = -32.9530, 92.9866
    test_time = "2014-03-08T00:00:00"  
    real_wind_path = "./data/era5_winds_march2014.nc" 

    print("  Comparing aerodynamic leeway advection across debris classes...")
    
    if os.path.exists(real_wind_path):
        for profile in ["low_windage", "mid_windage", "high_windage"]:
            lat_out, lon_out = step_rk4_multi_leeway_drift(test_lat, test_lon, test_time, 3600, profile, real_wind_path)
            print(f"  Class: {profile:<12} | New Position: {lat_out:.4f}°S, {lon_out:.4f}°E")







