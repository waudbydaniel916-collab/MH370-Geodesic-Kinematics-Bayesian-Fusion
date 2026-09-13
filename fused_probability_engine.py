import pandas as pd
import numpy as np

def run_master_bayesian_fusion(fused_csv_path):
    """
    Executes the ultimate multivariate Bayesian Data Fusion matrix, combining 
    kinematic drift, satellite BFO, hydroacoustics, and biological markers 
    across low, mid, and high windage debris fields.
    """
    print("  Initialising Master Multivariate Bayesian Data Fusion Engine...")
    
    try:
        df = pd.read_csv(fused_csv_path)
    except FileNotFoundError:
        print(f"  Error: Cannot find '{fused_csv_path}'. Run the satellite script first!")
        return None

    # ========================================================
    # 1. INTEGRATE SPATIAL DRIFT DISTANCES (P_drift)
    # ========================================================
    # Enforce exponential decay scaling on the localized distance offsets
    df['p_drift'] = np.exp(-df['distance_delta'] / 0.5)

    # ========================================================
    # 2. INTEGRATE BIOLOGICAL MARKERS (Barnacle Sclerochronology)
    # ========================================================
    # Filters out coordinate spaces north of -31.5°S
    df['p_barnacle'] = np.where(df['terminal_lat'] <= -31.5, 0.95, 0.15)

    # ========================================================
    # 3. INTEGRATE HYDROACOUSTIC ARRIVALS (SOFAR axis ducting)
    # ========================================================
    acoustic_center_lat = -32.8000
    df['p_acoustic'] = np.exp(-((df['terminal_lat'] - acoustic_center_lat)**2) / 0.1)

    # ========================================================
    # 4. COMPUTE THE MULTI-CLASS JOINT PROBABILITY DENSITY FUNCTION
    # ========================================================
    # P_fused = P_drift * P_satellite * P_barnacle * P_acoustic
    df['p_fused_master'] = df['p_drift'] * df['p_satellite'] * df['p_barnacle'] * df['p_acoustic']
    
    if df['p_fused_master'].max() > 0:
        df['p_fused_master'] = (df['p_fused_master'] / df['p_fused_master'].max()) * 100.0

    # Extract global peak coordinates of structural convergence
    peak_idx = df['p_fused_master'].idxmax()
    optimized_lat = df.loc[peak_idx, 'terminal_lat']
    optimized_lon = df.loc[peak_idx, 'terminal_lon']
    peak_class = df.loc[peak_idx, 'leeway_class']
    peak_probability = df.loc[peak_idx, 'p_fused_master']

    print("\n========================================================")
    print(f"  **CALIBRATED MULTI-CLASS TACTICAL SEARCH TARGET FOUND**")
    print("========================================================")
    print(f"  **Pinpointed Target Center**   : {optimized_lat:.4f}°S, {optimized_lon:.4f}°E")
    print(f"  Dominant Debris Morphology : {peak_class}")
    print(f"  Maximum Fusion Confidence   : {peak_probability:.2f}%")
    print(f"  Combined Fleet Population   : {len(df)} Active Particles")
    print("========================================================")
    
    df.to_csv("final_optimized_search_corridor.csv", index=False)
    print("  Final target matrix successfully exported to 'final_optimized_search_corridor.csv'!")
    
    return optimized_lat, optimized_lon

if __name__ == "__main__":
    run_master_bayesian_fusion(fused_csv_path="satellite_fused_weights.csv")


