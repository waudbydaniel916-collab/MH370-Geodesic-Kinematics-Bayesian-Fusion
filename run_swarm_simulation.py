import pandas as pd
import numpy as np
from datetime import datetime, timedelta
# Import your verified working step function from your file
from stochastic_drift import step_rk4_lagrangian_drift

def execute_particle_swarm_run(initial_lat, initial_lon, total_days=7, swarm_size=100):
    """
    Simulates a parallel ensemble of floating debris particles starting from a 
    specific candidate impact site to map spatial dispersion probabilities over time.
    """
    print(f"\n  Launching Monte Carlo drift ensemble (Swarm Size: {swarm_size})")
    print(f"  Initial Arc Anchor: {initial_lat:.4f}°S, {initial_lon:.4f}°E")
    
    # Initialize particle positions slightly spread around the starting point
    # representing initial debris scatter distributions
    lats = np.random.normal(initial_lat, 0.01, swarm_size)
    lons = np.random.normal(initial_lon, 0.01, swarm_size)
    
    # Timeline parameters
    start_time = datetime(2014, 3, 8, 0, 0, 0)
    dt_seconds = 3600  # 1 hour steps
    total_steps = int((total_days * 24 * 3600) / dt_seconds)
    alpha = 0.03       # Standard 3% wind leeway factor
    nc_path = "historical_hindcast.nc"
    
    current_time = start_time
    
    # Process time sequence forward
    for step in range(total_steps):
        # Format the time string to match your NetCDF dataset's temporal dimensions
        time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Advance each particle in the swarm through the fluid dynamic vector fields
        for i in range(swarm_size):
            try:
                lats[i], lons[i] = step_rk4_lagrangian_drift(
                    lat=lats[i],
                    lon=lons[i],
                    current_time_str=time_str,
                    dt=dt_seconds,
                    alpha=alpha,
                    netcdf_filepath=nc_path
                )
            except Exception as e:
                # If a particle drifts out of your NetCDF matrix bounds, break out early
                continue
                
        # Advance clock by 1 hour
        current_time += timedelta(seconds=dt_seconds)
        
        if step % 24 == 0:
            print(f" ⏱  Simulated Day {step//24 + 1}/{total_days} | Vector Target Clock: {time_str}")

    # Compile the final coordinate results matrix
    results_df = pd.DataFrame({
        'particle_id': range(swarm_size),
        'terminal_lat': lats,
        'terminal_lon': lons
    })
    
    output_filename = "bayesian_results.csv"
    results_df.to_csv(output_filename, index=False)
    print(f"\n  Swarm simulation complete! Final coordinates saved to '{output_filename}'")
    
    # Display the physical variance of the final particle footprint
    print(f"  Projected Swarm Center: {lats.mean():.4f}°S, {lons.mean():.4f}°E")
    print(f"  Footprint Spread Radius: Lat Var({lats.std():.4f}), Lon Var({lons.std():.4f})")
    
    return results_df

if __name__ == "__main__":
    # Test a 3-day flight simulation sweep starting from your project's anchor point
    execute_particle_swarm_run(initial_lat=-32.9530, initial_lon=92.9866, total_days=3, swarm_size=50)
