import pandas as pd
import numpy as np
from scipy.stats import norm

def evaluate_satellite_bfo_likelihood(csv_input_path, actual_bfo_hz=177.80, dynamic_variance=5.0):
    """
    Applies a Bayesian probability distribution curve over the simulated particles,
    scoring them based on how closely their coordinates line up with historical 
    Inmarsat Doppler shift frequencies across separate leeway profiles.
    """
    print(f"  Processing Inmarsat BFO alignment profile against target lock: {actual_bfo_hz} Hz")
    
    try:
        df = pd.read_csv(csv_input_path)
    except FileNotFoundError:
        print(f"  Error: Cannot find '{csv_input_path}'. Run your swarm simulation first!")
        return None

    # Track distances to center for data continuity in the pipeline
    benchmark_lat = -32.9530
    benchmark_lon = 92.9866
    df['distance_delta'] = np.sqrt((df['terminal_lat'] - benchmark_lat)**2 + (df['terminal_lon'] - benchmark_lon)**2)

    # Calculate Doppler shift as a function of geographic placement
    simulated_bfos = 182.5 + (df['terminal_lat'] * 0.12) - ((df['terminal_lon'] - 90.0) * 0.25)
    df['simulated_bfo_hz'] = simulated_bfos

    # Apply Gaussian Probability Density Function (PDF)
    bfo_probabilities = norm.pdf(df['simulated_bfo_hz'], loc=actual_bfo_hz, scale=dynamic_variance)
    
    if bfo_probabilities.max() > 0:
        bfo_probabilities = bfo_probabilities / bfo_probabilities.max()
    df['p_satellite'] = bfo_probabilities

    print("\n========================================================")
    print(f"  MULTI-CLASS INMARSAT BFO ALIGNMENT SUMMARY")
    print("========================================================")
    print(f"  Total Fleet Particles Analyzed : {len(df)}")
    
    # Break down tracking affinity metrics per debris morphology class
    for current_class in df['leeway_class'].unique():
        sub_group = df[df['leeway_class'] == current_class]
        high_affinity = len(sub_group[sub_group['p_satellite'] > 0.75])
        mean_prob = sub_group['p_satellite'].mean()
        print(f"  Class: {current_class:<13} | High-Affinity: {high_affinity}/{len(sub_group)} | Mean P: {mean_prob * 100:.2f}%")
        
    print("========================================================")
    
    # Export unified tracking parameters
    output_filename = "satellite_fused_weights.csv"
    df.to_csv(output_filename, index=False)
    print(f"  Fused multi-class satellite telemetry profiles saved to '{output_filename}'")
    return df['p_satellite'].mean()

if __name__ == "__main__":
    evaluate_satellite_bfo_likelihood(csv_input_path="bayesian_results.csv", actual_bfo_hz=177.80)

