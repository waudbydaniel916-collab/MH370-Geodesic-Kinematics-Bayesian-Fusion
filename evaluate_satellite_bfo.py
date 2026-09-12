import pandas as pd
import numpy as np
from scipy.stats import norm

def evaluate_satellite_bfo_likelihood(csv_input_path, actual_bfo_hz=177.80, dynamic_variance=5.0):
    """
    Applies a Bayesian probability distribution curve over the simulated particles,
    scoring them based on how closely their coordinates line up with historical 
    Inmarsat Doppler shift frequencies.
    """
    print(f"  Processing Inmarsat BFO alignment profile against target lock: {actual_bfo_hz} Hz")
    
    try:
        df = pd.read_csv(csv_input_path)
    except FileNotFoundError:
        print(f"  Error: Cannot find '{csv_input_path}'. Run your swarm simulation first!")
        return None

    # Define an empirical function simulating the satellite geometry tracking curve.
    # In reality, this correlates to the relative velocity vector between the plane and the satellite.
    # For this matrix, we map it as a function of the local spatial grid coordinates.
    simulated_bfos = 182.5 + (df['terminal_lat'] * 0.12) - ((df['terminal_lon'] - 90.0) * 0.25)
    df['simulated_bfo_hz'] = simulated_bfos

    # Apply a Gaussian Probability Density Function (PDF)
    # This weights particles near 177.8 Hz highly, and scales down distant outliers
    bfo_probabilities = norm.pdf(df['simulated_bfo_hz'], loc=actual_bfo_hz, scale=dynamic_variance)
    
    # Normalize probabilities to a 0.0 - 1.0 scale
    if bfo_probabilities.max() > 0:
        bfo_probabilities = bfo_probabilities / bfo_probabilities.max()
    df['p_satellite'] = bfo_probabilities

    mean_p_sat = df['p_satellite'].mean()

    print("\n========================================================")
    print(f"  INMARSAT BFO ALIGNMENT MATRIX SUMMARY")
    print("========================================================")
    print(f"  Total Fleet Particles Analyzed : {len(df)}")
    print(f"  High-Affinity Particle Count   : {len(df[df['p_satellite'] > 0.75])}")
    print(f"  Mean Satellite Probability Weight : {mean_p_sat * 100:.2f}%")
    print("========================================================")
    
    # Export the combined tracking weights
    df.to_csv("satellite_fused_weights.csv", index=False)
    print("  Fused satellite telemetry profiles saved to 'satellite_fused_weights.csv'")
    return mean_p_sat

if __name__ == "__main__":
    evaluate_satellite_bfo_likelihood(
        csv_input_path="bayesian_results.csv",
        actual_bfo_hz=177.80
    )
