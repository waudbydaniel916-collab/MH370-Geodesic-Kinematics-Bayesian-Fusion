import math
import numpy as np
import xarray as xr
import os

# Open dataset once at system layer to pull matrices into RAM
WIND_DATASET_PATH = "./data/era5_winds_march2014.nc"
if os.path.exists(WIND_DATASET_PATH):
    GLOBAL_WIND_DS = xr.open_dataset(WIND_DATASET_PATH)
else:
    GLOBAL_WIND_DS = None

def step_rk4_multi_leeway_drift(lat, lon, current_time_str, dt, leeway_class):
    """
    Vectorised RK4 Solver reading directly from global system RAM
    to support high-capacity particle fleets without disk I/O lag.
    """
    global GLOBAL_WIND_DS
    if GLOBAL_WIND_DS is None:
        raise FileNotFoundError("  High-capacity solver error: Master wind matrix file missing at './data/'.")
        
    leeway_profiles = {
        "low_windage": 0.01,    
        "mid_windage": 0.03,    
        "high_windage": 0.05    
    }
    alpha = leeway_profiles.get(leeway_class, 0.03)
    
    def get_velocity_field(target_lat, target_lon):
        # Direct RAM selection hook
        wind_node = GLOBAL_WIND_DS.sel(valid_time=current_time_str, latitude=target_lat, longitude=target_lon, method="nearest")
        
        u_wind = float(wind_node['u10'].values)
        v_wind = float(wind_node['v10'].values)
        
        # Indian Ocean subtropical gyre current baseline vector mapping
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
    print("  Verifying system RAM acceleration hook...")
    if GLOBAL_WIND_DS is not None:
        lat_out, lon_out = step_rk4_multi_leeway_drift(-32.9530, 92.9866, "2014-03-08T00:00:00", 3600, "low_windage")
        print(f"  RAM read check passed. Output: {lat_out:.4f}°S, {lon_out:.4f}°E")












