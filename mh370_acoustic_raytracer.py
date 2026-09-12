import numpy as np

def calculate_marian_sound_speed(depth, latitude):
    z_sofar = 1000.0  
    c_sofar = 1482.0  
    epsilon = 2.0 * (depth - z_sofar) / z_sofar
    return c_sofar * (1.0 + 0.0074 * (epsilon - 1.0 + np.exp(-epsilon)))

def compute_dynamic_travel_time(geodesic_distance_km):
    """
    Evaluates wave velocity horizontally directly inside the SOFAR channel axis duct.
    """
    # Pin wave propagation strictly to the SOFAR axis center depth layer (1000m)
    effective_sound_speed = calculate_marian_sound_speed(depth=1000.0, latitude=-32.8)
    
    distance_meters = geodesic_distance_km * 1000.0
    total_seconds = distance_meters / effective_sound_speed
    
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    
    return minutes, seconds, effective_sound_speed

mins, secs, avg_v = compute_dynamic_travel_time(2054.22)
print(f"HA01 Axis-Trapped Propagation: {mins} mins, {secs:.3f} secs (Axis V: {avg_v:.2f} m/s)")

