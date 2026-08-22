import os
import numpy as np
from pyproj import Geod

print("[SYSTEM] Initializing Kinematic Glide Extension Trajectory Engine...")

# 1. CORE SIMULATOR ACCORD COORDINATES
# True historical simulator data coordinates recovered from hard drive fragments
sim_exhaustion_lat = -45.0000
sim_exhaustion_lon = 104.0000
CRUISE_ALTITUDE_FT = 38000.0  # Initial altitude at fuel exhaustion step

# Standard aerodynamic constants for a Boeing 777-200ER airframe
GLIDE_RATIO = 16.0             # 16:1 Lift-to-Drag glide efficiency ratio
METERS_PER_FOOT = 0.3048

# Initialize professional WGS84 geodesic engine
geod = Geod(ellps='WGS84')

print(f"[INPUT] Simulator Fuel Exhaustion Point: {sim_exhaustion_lat:.4f}°S, {sim_exhaustion_lon:.4f}°E")
print(f"[PHYSICS] Airframe glide profile ratio configured at: {GLIDE_RATIO}:1 bounds\n")

# 2. GLIDE RANGE EXTENSION CALCULATIONS
print("="*75)
print("✈️ AERODYNAMIC GLIDE PATH SOLVER LOG WINDOW")
print("="*75)

# Convert initial altitude to meters
altitude_meters = CRUISE_ALTITUDE_FT * METERS_PER_FOOT

# Calculate total forward sliding glide range distance (m = altitude * ratio)
max_glide_distance_m = altitude_meters * GLIDE_RATIO
max_glide_distance_km = max_glide_distance_m / 1000.0

# Project 4 unique manual heading vectors to establish a spatial bounding box
headings = [0.0, 90.0, 180.0, 270.0]  # North, East, South, West bounds
boundary_points = []

for heading in headings:
    # Calculate target endpoints sliding outward using WGS84 forward solving
    end_lon, end_lat, _ = geod.fwd(sim_exhaustion_lon, sim_exhaustion_lat, heading, max_glide_distance_m)
    boundary_points.append((end_lat, end_lon))

print(f"  └─ Initial Flameout Altitude : {CRUISE_ALTITUDE_FT:.0f} Feet ({altitude_meters:.1f} Meters)")
print(f"  └─ Maximum Air Glide Range  : {max_glide_distance_km:.2f} Kilometers")

print(f"\n🚀 EXTENDED GLIDE PROFILE CORRIDOR BOUNDS:")
print(f"  └─ North Boundary Limit     : {boundary_points[0][0]:.4f}°S, {boundary_points[0][1]:.4f}°E")
print(f"  └─ East Boundary Limit      : {boundary_points[1][0]:.4f}°S, {boundary_points[1][1]:.4f}°E")
print(f"  └─ South Boundary Limit     : {boundary_points[2][0]:.4f}°S, {boundary_points[2][1]:.4f}°E")
print(f"  └─ West Boundary Limit      : {boundary_points[3][0]:.4f}°S, {boundary_points[3][1]:.4f}°E")
print("="*75)

# 3. EXPORT STRUCTURED GLIDE TRACK PATH DATA SHEET
base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
csv_out_path = os.path.join(base_dir, 'glide_extension_results.csv')

import csv
with open(csv_out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Boundary Parameter', 'Latitude (Decimal)', 'Longitude (Decimal)', 'Glide Distance Max (km)'])
    names = ['North Bound', 'East Bound', 'South Bound', 'West Bound']
    for idx, name in enumerate(names):
        writer.writerow([name, f"{boundary_points[idx][0]:.4f}", f"{boundary_points[idx][1]:.4f}", f"{max_glide_distance_km:.2f}"])

print(f"\n[SUCCESS] Glide expansion metrics exported flawlessly to: {csv_out_path}\n")
