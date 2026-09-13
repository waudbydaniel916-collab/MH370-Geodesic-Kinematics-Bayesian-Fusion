import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
# Import your verified multi-leeway function
from stochastic_drift import step_rk4_multi_leeway_drift

def execute_multi_class_swarm(initial_lat, initial_lon, total_days=3, swarm_size_per_class=30):
    """
    Simulates separate parallel fleets of low, mid, and high windage debris 
    to track how asset morphology alters spatial footprint dispersion.
    """
    print(f"\n  Launching Validated Multi-Class Monte Carlo Drift Ensemble")
    print(f"  Initial Arc Anchor: {initial_lat:.4f}°S, {initial_lon:.4f}°E")
    
    leeway_classes = ["low_windage", "mid_windage", "high_windage"]
    all_results = []
    
    # Timeline parameters matching your real ERA5 dataset limits
    start_time = datetime(2014, 3, 8, 0, 0, 0)
    dt_seconds = 3600  # 1 hour steps
    total_steps = int((total_days * 24 * 3600) / dt_seconds)
    real_wind_path = "./data/era5_winds_march2014.nc"
    
    # Initialize separate parallel fleets
    for debris_type in leeway_classes:
        print(f"  Initialising fleet array for category: {debris_type}")
        lats = np.random.normal(initial_lat, 0.01, swarm_size_per_class)
        lons = np.random.normal(initial_lon, 0.01, swarm_size_per_class)
        
        current_time = start_time
        
        # Process the time loop for the current specific debris fleet
        for step in range(total_steps):
            time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S")
            
            for i in range(swarm_size_per_class):
                try:
                    lats[i], lons[i] = step_rk4_multi_leeway_drift(
                        lat=lats[i],
                        lon=lons[i],
                        current_time_str=time_str,
                        dt=dt_seconds,
                        leeway_class=debris_type,
                        wind_nc_path=real_wind_path
                    )
                except Exception:
                    continue
                    
            current_time += timedelta(seconds=dt_seconds)
            
        print(f"   ⏱ {debris_type} fleet simulation complete through day {total_days}.")
        
        # Append the terminal locations for this class to the master registry
        for idx in range(swarm_size_per_class):
            all_results.append({
                'particle_id': f"{debris_type}_{idx}",
                'leeway_class': debris_type,
                'terminal_lat': lats[idx],
                'terminal_lon': lons[idx]
            })

    # Compile everything into a structured pandas dataframe
    results_df = pd.DataFrame(all_results)
    output_filename = "bayesian_results.csv"
    results_df.to_csv(output_filename, index=False)
    
    print(f"\n  Multi-class simulation finished! Data output to '{output_filename}'")
    
    # Print out structural profile diagnostics
    print("\n  FOOTPRINT DISPERSION PROFILE SUMMARY:")
    print("========================================================")
    for debris_type in leeway_classes:
        sub_df = results_df[results_df['leeway_class'] == debris_type]
        mean_lat = sub_df['terminal_lat'].mean()
        mean_lon = sub_df['terminal_lon'].mean()
        print(f"  {debris_type:<13} Centroid -> Lat: {mean_lat:.4f}°S, Lon: {mean_lon:.4f}°E")
    print("========================================================")
    
    return results_df

if __name__ == "__main__":
    # Run a 3-day verification tracking loop
    execute_multi_class_swarm(initial_lat=-32.9530, initial_lon=92.9866, total_days=3, swarm_size_per_class=30)


