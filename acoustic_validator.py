import os
import numpy as np
from pyproj import Geod

# =========================================================================
# 1. CORE CONFIGURATION & GEOSPATIAL COORDINATES
# =========================================================================
print("[SYSTEM] Initializing Hydroacoustic Signal Verification Engine...")

# Pinpointed target core center from your Bayesian Drift Model
crash_lat = -32.9530
crash_lon = 92.9866

# Verified scientific coordinates of CTBTO Hydrophone Stations
hydrophone_stations = [
    {"name": "Station HA01 (Cape Leeuwin, Australia)", "lat": -34.3050, "lon": 115.1110},
    {"name": "Station H08 (Diego Garcia, Indian Ocean)", "lat": -7.3150, "lon": 72.4210}
]

# Average speed of sound in the deep-sea SOFAR channel (meters per second)
SOUND_SPEED_MPS = 1482.0 

# Initialize the professional WGS84 ellipsoid geodesic engine
geod = Geod(ellps='WGS84')

print(f"[INPUT] Evaluating Bayesian Crash Epicenter: {crash_lat:.4f}°S, {crash_lon:.4f}°E")
print(f"[PHYSICS] Fixed SOFAR channel sound propagation velocity set to: {SOUND_SPEED_MPS} m/s\n")

# =========================================================================
# 2. WAVEFORM PROPAGATION SPEED & TIME CALCULATIONS
# =========================================================================
print("="*75)
print("  CRITICAL WAVEFORM ARRIVAL WINDOWS (GEOLOGICAL FILTER ACTIVE)")
print("="*75)

for station in hydrophone_stations:
    # Calculate the absolute shortest path distance over Earth's curved surface
    _, _, distance_meters = geod.inv(crash_lon, crash_lat, station["lon"], station["lat"])
    distance_km = distance_meters / 1000.0
    
    # Calculate travel time in total seconds
    travel_time_seconds = distance_meters / SOUND_SPEED_MPS
    
    # Format total seconds into human-readable Minutes and Seconds
    minutes = int(travel_time_seconds // 60)
    seconds = int(travel_time_seconds % 60)
    milliseconds = int((travel_time_seconds - int(travel_time_seconds)) * 1000)
    
    print(f"\n  {station['name']}")
    print(f"  └─ Exact Geodesic Distance : {distance_km:.2f} km")
    print(f"  └─ Calculated Travel Time   : {minutes} mins, {seconds}.{milliseconds:03d} secs")
    print(f"  └─ Targeted Signal Filter   : Fast-forward logs to baseline event + {minutes}m {seconds}s")
    print(f"  └─ Forensic Note            : Disregard louder macro-seismic activity around this window.")

print("\n" + "="*75)

# =========================================================================
# 3. DIRECT DATA LINK PREPARATION
# =========================================================================
base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
csv_out_path = os.path.join(base_dir, 'hydroacoustic_results.csv')

print(f"[EXPORT] Ready to output micro-window targeted sweeps to: {csv_out_path}")

# Initialize database template for future micro-signal tracking
if not os.path.exists(csv_out_path):
    import csv
    with open(csv_out_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Station Name', 'Geodesic Distance (km)', 'Travel Time (seconds)', 'Target Signal Status'])
        for station in hydrophone_stations:
            _, _, dist_m = geod.inv(crash_lon, crash_lat, station["lon"], station["lat"])
            t_sec = dist_m / SOUND_SPEED_MPS
            writer.writerow([station['name'], f"{dist_m/1000.0:.2f}", f"{t_sec:.3f}", 'Pending Background Micro-Audit'])
    print("[SUCCESS] Acoustic results spreadsheet skeleton initialized perfectly.")
else:
    print("[SYSTEM] Active hydroacoustic_results.csv detected. Structured data sync ready.")
