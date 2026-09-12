import pandas as pd
import numpy as np

def calculate_swarm_density_weights(csv_input_path, benchmark_lat, benchmark_lon, proximity_radius_deg=0.5):
    """
    Evaluates terminal particle locations against key baseline coordinates 
    (like the 7th Arc intercept zones or verified debris discovery sites).
    """
    print(f"  Analyzing particle landing density relative to benchmark: {benchmark_lat}°S, {benchmark_lon}°E")
    
    try:
        # Load your freshly generated Monte Carlo drift results
        df = pd.read_csv(csv_input_path)
    except FileNotFoundError:
        print(f"  Error: Cannot find '{csv_input_path}'. Run your swarm simulation first!")
        return None

    # Calculate absolute spatial distance errors from our targeted benchmark node
    lat_errors = df['terminal_lat'] - benchmark_lat
    lon_errors = df['terminal_lon'] - benchmark_lon
    
    # Compute simple Euclidean coordinate distances (convertible to geodesic km)
    distances = np.sqrt(lat_errors**2 + lon_errors**2)
    df['distance_delta'] = distances
    
    # Apply an indicator function: evaluate how many particles hit within our search threshold zone
    intercepting_particles = df[df['distance_delta'] <= proximity_radius_deg]
    
    # Calculate the raw drift probability matrix score (P_drift)
    p_drift = len(intercepting_particles) / len(df)
    
    print("\n========================================================")
    print(f"  GRID EVALUATION SUMMARY FOR SEARCH MATRIX")
    print("========================================================")
    print(f"  Total Ensemble Particles Evaluated : {len(df)}")
    print(f"  Particles Intercepting Search Zone : {len(intercepting_particles)}")
    print(f"  Calculated Drift Likelihood (P_drift) : {p_drift * 100:.2f}%")
    print("========================================================")
    
    # Save the processed density payload back for the main fusion engine
    df.to_csv("processed_density_weights.csv", index=False)
    return p_drift

if __name__ == "__main__":
    # Test your particle results against your pinpointed project center
    calculate_swarm_density_weights(
        csv_input_path="bayesian_results.csv",
        benchmark_lat=-32.9530,
        benchmark_lon=92.9866,
        proximity_radius_deg=0.3
    )
