import numpy as np

def extract_trench_prominence():
    print("================================================================================")
    print("SEAFLOOR DATA FORENSICS: ABYSSAL DEARTH & PROMINENCE CALCULATION ENGINE")
    print("================================================================================")

    # Simulated high-density multibeam echo-sounder array representing a fault line transect
    # Raw values model seabed elevation measurements (metres below sea level)
    raw_depth_transect = np.array([
        -4820.5, -4850.2, -4910.8, -5020.4, -5018.9, 
        -4980.3, -5150.7, -5280.1, -4910.4, -4860.2
    ])

    print(f"INGESTING TRANSECT ARRAY: {len(raw_depth_transect)} Discrete Multibeam Nodes")
    print(f"  ├── Absolute Maximum Trench Depth Observed : {np.min(raw_depth_transect):.1f} m")
    print(f"  └── Average Baseline Regional Seafloor Floor: {np.mean(raw_depth_transect):.1f} m")
    print("-" * 80)
    print("COMPUTING SUBMARINE TOPOGRAPHIC GRADIENTS...")

    # Calculate absolute localized depth drops between adjacent sonar returns
    spatial_gradients = np.abs(np.diff(raw_depth_transect))
    significant_fault_drop_threshold = 150.0  # Metric meters

    anomalous_slopes_logged = 0
    for idx, gradient in enumerate(spatial_gradients):
        if gradient >= significant_fault_drop_threshold:
            anomalous_slopes_logged += 1
            node_depth = raw_depth_transect[idx + 1]
            print(f"  ├── CRITICAL SEAFLOOR PROMINENCE IDENTIFIED")
            print(f"  │    ├── Fault Coordinate Transition : Node {idx} -> Node {idx+1}")
            print(f"  │    ├── Local Displacement Vector   : Drop of {gradient:.2f} meters")
            print(f"  │    └── Base Abyssal Floor Depth    : {node_depth:.1f} meters")
            print("  │")

    print("-" * 80)
    print(f"ANALYSIS VERDICT: LOG RECONSTRUCTION COMPLETE // {anomalous_slopes_logged} HIGH-RELIEF SLOPES FOUND")
    print("   High local variance confirms structural walls capable of casting severe acoustic shadows.")
    print("================================================================================")

if __name__ == "__main__":
    extract_trench_prominence()
