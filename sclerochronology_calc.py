import numpy as np
import pandas as pd

def execute_biological_growth_filter(input_path="satellite_fused_weights.csv", output_path="processed_density_weights.csv"):
    """
    Evaluates drift track terminal spaces against marine barnacle growth criteria.
    Maps thermal thresholds to determine physical survival probabilities.
    """
    print(f"Loading satellite-weighted matrix data from: {input_path}")
    df = pd.read_csv(input_path)
    n_particles = len(df)
    
    print(f"Evaluating biological constraints across {n_particles} tracking coordinates...")
    
    terminal_lat = df['terminal_lat'].values
    
    # 1. Biological Temperature Gradient Model
    # Lepas anatifera barnacles require specific thermal zones.
    # Southern water configurations cooler than -31.5 degrees latitude impact metabolism.
    # Rather than a hard cut-off, we implement a cumulative sigmoidal probability distribution curve.
    
    transition_latitude = -31.5
    thermal_steepness_factor = 0.4  # Dictates how sharply the survival probability drops off north/south
    
    # Vectorized execution of the logistic probability curve across all active points
    # Particles located far north of the transition zone scale down to low likelihoods
    biological_probabilities = 1.0 / (1.0 + np.exp((terminal_lat - transition_latitude) / thermal_steepness_factor))
    
    # 2. Integrate Cumulative Spatial Weights
    # Combine satellite tracking metrics with biological limits 
    if 'satellite_probability_weight' in df.columns:
        combined_fused_weight = df['satellite_probability_weight'].values * biological_probabilities
    else:
        combined_fused_weight = biological_probabilities
        
    # Normalise weights to preserve spatial scaling limits
    if np.max(combined_fused_weight) > 0:
        combined_fused_weight = combined_fused_weight / np.max(combined_fused_weight)
        
    # 3. Export Comprehensive Data Matrix
    df['barnacle_survival_probability'] = biological_probabilities
    df['fused_drift_sat_barnacle_weight'] = combined_fused_weight
    
    df.to_csv(output_path, index=False)
    print(f"Biological growth constraint matrix successfully saved to: {output_path}")
    
    # Calculate top probability target cluster center to display verification values
    top_indices = np.argsort(combined_fused_weight)[-100:]  # Average across the top 100 convergence coordinates
    mean_lat = np.mean(df['terminal_lat'].iloc[top_indices])
    mean_lon = np.mean(df['terminal_lon'].iloc[top_indices])
    print(f"Current Peak Convergence Zone Estimate: Latitude {mean_lat:.4f}, Longitude {mean_lon:.4f}")

if __name__ == "__main__":
    execute_biological_growth_filter()

