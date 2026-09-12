import numpy as np

def calculate_marian_sound_speed(depth, latitude):
    """
    Computes an empirical local water column sound velocity profile (SST to Seafloor).
    Accounts for thermocline variations and hydrostatic deep-sea pressures.
    """
    # Deep ocean baseline parameters
    z_sofar = 1000.0  # SOFAR axis depth center in meters
    c_sofar = 1482.0  # Speed of sound at axis channel center (m/s)
    
    # Normalized depth scale relative to the SOFAR axis channel
    epsilon = 2.0 * (depth - z_sofar) / z_sofar
    # Munk Sound Profile equation modeling acoustic waveguide trapping
    c_depth = c_sofar * (1.0 + 0.0074 * (epsilon - 1.0 + np.exp(-epsilon)))
    return c_depth

def compute_dynamic_travel_time(geodesic_distance_km, average_depth_m=3500.0):
    """
    Integrates progressive travel times across dynamic ocean acoustic sound speeds
    instead of flat-line vacuum variables.
    """
    # Generate integrated depth samples along the sound path profile
    depth_samples = np.linspace(0, average_depth_m, 100)
    sound_speeds = calculate_marian_sound_speed(depth_samples, latitude=-32.8)
    
    # Determine the mean practical horizontal sound propagation speed in the channel
    effective_sound_speed = np.mean(sound_speeds)
    
    distance_meters = geodesic_distance_km * 1000.0
    total_seconds = distance_meters / effective_sound_speed
    
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    
    return minutes, seconds, effective_sound_speed

# Example tracking run to Station HA01 (Cape Leeuwin)
mins, secs, avg_v = compute_dynamic_travel_time(2054.22)
print(f"HA01 Corrected Acoustic Propagation: {mins} mins, {secs:.3f} secs (Effective V: {avg_v:.2f} m/s)")
