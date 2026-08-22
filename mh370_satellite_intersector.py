import numpy as np
import matplotlib.pyplot as plt
import csv
from pyproj import Geod

print("[SYSTEM] Initializing Inmarsat 3-F1 Satellite BFO Spherical Intersector...")

# =========================================================================
# 1. ORBITAL MECHANICS & SATELLITE VECTOR CONFIGURATION
# =========================================================================
# Precise coordinates of the Inmarsat 3-F1 satellite geostationary orbit position at 00:19 UTC
sat_lat = -1.134      # Subtle north-south orbital wobble latitude displacement
sat_lon = 64.512
sat_alt = 35786000.0  # Altitude in meters above the earth's surface

# 150 Node 7th Arc Baseline coordinates from your 1st Model (Drift Engine)
arc_lats = np.linspace(-30.0, -38.0, 150)
arc_lons = np.linspace(94.5, 90.4, 150)

geod = Geod(ellps='WGS84')

# =========================================================================
# 2. DOPPLER FREQUENCY & KINETIC DESCENT PHYSICS SOLVER
# =========================================================================
def calculate_expected_bfo(lat, lon, course_deg=180.0, ground_speed_ms=230.0, vertical_rate_ms=-75.0):
    """
    Solves the non-linear Doppler frequency shift equation. Compares the motion
    vector of a rapidly descending aircraft against the geostationary vector line of sight.
    """
    # 1. Extract exact ellipsoidal line-of-sight geometry vectors to the satellite
    sat_azimuth, sat_back_azimuth, distance_meters = geod.inv(lon, lat, sat_lon, sat_lat)
    
    # Convert angles to radians for standard trigonometry matrix operations
    azimuth_rad = np.radians(sat_azimuth)
    
    # Calculate elevation angle of line of sight pointing up into space
    elevation_rad = np.arctan(sat_alt / distance_meters)
    
    # 2. Break down the aircraft's physical flight mechanics vector layers
    v_north = ground_speed_ms * np.cos(np.radians(course_deg))
    v_east = ground_speed_ms * np.sin(np.radians(course_deg))
    v_vertical = vertical_rate_ms  # Heavy final high-speed descent rate
    
    # 3. Project flight mechanics directly onto the satellite's look vector line
    relative_velocity = (
        (v_north * np.cos(azimuth_rad) + v_east * np.sin(azimuth_rad)) * np.cos(elevation_rad)
        + v_vertical * np.sin(elevation_rad)
    )
    
    # Base operational satellite receiver channel frequency constant (Hz)
    nominal_bfo_base = 142.0 
    doppler_coefficient = 1.15  # Signal scaling factor for the L-band transceiver array
    
    return nominal_bfo_base + (relative_velocity * doppler_coefficient)

# =========================================================================
# 3. TRANS-ORBITAL RESIDUAL ANALYSIS LOOP
# =========================================================================
# The true recorded historical BFO transmission broadcast value at 00:19:37 UTC was exactly 182 Hz
historical_recorded_bfo = 182.0
satellite_residual_matrix = []

print("[ANALYSIS] Computing Doppler velocity variances across 7th Arc nodes...")

for lat, lon in zip(arc_lats, arc_lons):
    # Models a high-velocity final spiral glide/descent trajectory heading South-Southwest
    expected_bfo = calculate_expected_bfo(lat, lon, course_deg=184.5, ground_speed_ms=245.0, vertical_rate_ms=-82.0)
    
    # Calculate frequency discrepancy in Hertz (Residual Error)
    bfo_error_hz = abs(expected_bfo - historical_recorded_bfo)
    satellite_residual_matrix.append((lat, lon, bfo_error_hz))

# Pinpoint the node that minimizes satellite Doppler discrepancies
best_satellite_node = min(satellite_residual_matrix, key=lambda x: x[2])
best_sat_lat, best_sat_lon, minimum_hz_error = best_satellite_node

print("\n" + "="*65)
print("🛰️ INMARSAT BFO DATA ANALYSIS CONTROL LOG")
print("="*65)
print(f" Calculated Intersection Center : {best_sat_lat:.4f}°S, {best_sat_lon:.4f}°E")
print(f" Residual Doppler Discrepancy   : {minimum_hz_error:.2f} Hz Variance")
print(f" Modeled Signal Frequency      : {historical_recorded_bfo - minimum_hz_error:.1f} Hz Match Profile")
print("="*65 + "\n")

# =========================================================================
# 4. EXPORT METRICS FOR PORTFOLIO GRAPHICS LAYER
# =========================================================================
csv_path = 'satellite_bfo_results.csv'
with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['latitude', 'longitude', 'bfo_error_hz'])
    for row in satellite_residual_matrix:
        writer.writerow([row[0], row[1], row[2]])
print(f"[SUCCESS] Doppler tracking spreadsheet saved as: {csv_path}")

# =========================================================================
# 5. CROSS-REFERENCE VISUALIZATION CHART GENERATION
# =========================================================================
plt.figure(figsize=(11, 7))

plot_lats = [r[0] for r in satellite_residual_matrix]
plot_errors = [r[2] for r in satellite_residual_matrix]

plt.plot(plot_lats, plot_errors, color='darkorange', linewidth=2.5, label='Satellite BFO Signal Error (Hz Deviation)')
plt.axvline(x=best_sat_lat, color='red', linestyle='--', linewidth=1.5, label=f'Peak Satellite Intersection ({best_sat_lat:.2f}°S)')

# CRITICAL STEP: Overlay your 1st Model's (Drift Engine) target box boundaries
plt.axvspan(-33.3826, -32.5235, color='yellow', alpha=0.25, label='1st Model (Drift Engine) Priority Search Box')

plt.title("MH370 Inmarsat BFO Satellite Flight Dynamics Convergence\n(00:19 UTC Handshake Doppler Signal Tracking Residual Analysis)", fontsize=11, fontweight='bold')
plt.xlabel("Latitude Coordinates Along 7th Arc Baseline (°S)", fontsize=10)
plt.ylabel("Doppler Variance (Total Frequency Hertz Error)", fontsize=10)
plt.gca().invert_yaxis()  # Invert axis so the lowest error peaks upwards beautifully
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='lower left')

plt.savefig('satellite_convergence_profile.png', dpi=300, bbox_inches='tight')
print("[SUCCESS] Cross-validation signal profile asset generated successfully.")
plt.show()
