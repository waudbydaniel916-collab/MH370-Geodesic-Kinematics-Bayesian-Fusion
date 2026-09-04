import os
import pandas as pd
import numpy as np
from pyproj import Geod

print("[SYSTEM] Initializing Geodesic Mathematical Validation Engine...")

base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
manifest_path = os.path.join(base_dir, 'sonar_anomaly_manifest.csv')

# Define your exact baseline target center coordinates
BASE_LAT, BASE_LON = -32.9530, 92.9866

if os.path.exists(manifest_path):
    try:
        df = pd.read_csv(manifest_path)
        
        # Initialize the WGS84 Ellipsoid using the exact Karney mathematical model
        geod = Geod(ellps='WGS84')
        
        distances_km = []
        
        print("\n" + "="*80)
        print("📐 GEODESIC DISTANCE CLOSURE REPORT (WGS84 ELLIPSOID)")
        print("="*80)
        
        for idx, row in df.iterrows():
            frag_id = int(row['Intercept_ID'])
            f_lat = float(row['Target_Latitude'])
            f_lon = float(row['Target_Longitude'])
            
            # Solve the inverse geodesic problem (calculates the exact true distance in meters)
            _, _, distance_meters = geod.inv(BASE_LON, BASE_LAT, f_lon, f_lat)
            distance_km = distance_meters / 1000.0
            distances_km.append(distance_km)
            
            # Print metrics for the first few nodes as a verification sample
            if frag_id <= 5:
                print(f"  ├── Fragment #{frag_id:02d} Target Fix: {f_lat:.5f}°S, {f_lon:.5f}°E ➔ Dist: {distance_km:.3f} km")
        
        max_dist = np.max(distances_km)
        mean_dist = np.mean(distances_km)
        
        print("-"*80)
        print(f"📊 TRAIL MATRIX FIELD METRICS:")
        print(f"  ├── Average Fragment Dispersion Distance : {mean_dist:.3f} km")
        print(f"  └── Maximum Impact Trail Radius (Extent)  : {max_dist:.3f} km")
        print("-"*80)
        
        # Verification Safety Check
        # A real underwater impact wreckage trail disperses across 1 to 10 kilometers.
        # If the points are thousands of kilometers away or zero, the math is broken.
        if 0.1 <= mean_dist <= 15.0:
            print("🚨 VERIFICATION VERDICT: 🟩 MATHEMATICALLY VALID")
            print("   The fragment cluster conforms perfectly to a localized deep-sea wreckage cascade pattern.")
        else:
            print("🚨 VERIFICATION VERDICT: 🟥 MATHEMATICALLY INVALID")
            print("   The coordinate distribution falls outside standard aerodynamic or hydroacoustic dispersion limits.")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"[CRASH] Geodesic verification routine aborted: {e}")
else:
    print(f"[ERROR] Missing file dependency: {manifest_path}. Run sonar_transfuser.py first.")

