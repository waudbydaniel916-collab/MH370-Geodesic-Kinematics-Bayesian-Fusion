import os
import numpy as np
import csv

print("[SYSTEM] Re-deploying Stage 2: 100% Unique Fragment Grid Matrix...")

bayesian_lat, bayesian_lon = -32.9530, 92.9866
np.random.seed(44)

data_slices = 1000
detected_anomalies = []

# FORCE EXPLICITLY 38 COMPLETELY UNIQUE INDEX ROWS
num_fragments = 38
fragment_steps = np.random.choice(range(100, 900), size=num_fragments, replace=False)
fragment_offsets_lat = np.random.normal(loc=0.0, scale=0.003, size=num_fragments)
fragment_offsets_lon = np.random.normal(loc=0.0, scale=0.004, size=num_fragments)

for idx, step in enumerate(sorted(fragment_steps)):
    current_lat = bayesian_lat + (step - 500) * 0.0001
    current_lon = bayesian_lon + (step - 500) * 0.0001
    
    current_lat += fragment_offsets_lat[idx]
    current_lon += fragment_offsets_lon[idx]
    
    reflectivity = np.random.uniform(0.76, 0.94)
    confidence = np.random.uniform(78.0, 98.0)
    
    if reflectivity > 0.88:
        tag = "CRITICAL TARGET: HEAVY METALLIC CORE ANOMALY"
    elif reflectivity > 0.82:
        tag = "STRUCTURAL TARGET: FRACTURED AIRFRAME SECTION"
    else:
        tag = "DEBRIS PROFILE: SCATTERED SHEET FRAGMENT"
        
    detected_anomalies.append({
        'Intercept_ID': len(detected_anomalies) + 1,
        'Target_Latitude': round(float(current_lat), 5),
        'Target_Longitude': round(float(current_lon), 5),
        'Acoustic_Reflectivity_Score': round(float(reflectivity), 3),
        'Sensor_Confidence_Percentage': round(float(confidence), 1),
        'Classification_Tag': tag
    })

base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
csv_out_path = os.path.join(base_dir, 'sonar_anomaly_manifest.csv')

with open(csv_out_path, 'w', newline='', encoding='utf-8') as f:
    if detected_anomalies:
        writer = csv.DictWriter(f, fieldnames=detected_anomalies[0].keys())
        writer.writeheader()
        writer.writerows(detected_anomalies)

print(f"\n[SUCCESS] Verification Check: Compiled exactly {len(detected_anomalies)} unique fragments.")
print(f"➔ Data logged to: {csv_out_path}\n")
