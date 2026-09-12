import math

def calculate_geodesic_search_box(center_lat, center_lon, target_area_km2, aspect_ratio=0.5):
    """
    Computes true geographic bounding corners based on a strict target area grid 
    accounting for the oblate convergence of meridians near the poles.
    """
    # Calculate box dimensions based on desired target area coverage
    # height * width = target_area_km2; aspect_ratio = width / height
    height_km = math.sqrt(target_area_km2 / aspect_ratio)
    width_km = target_area_km2 / height_km
    
    # Earth spatial degree scaling factor (approx 111,000 meters per degree lat)
    deg_per_km_lat = 1.0 / 111.0
    # Longitudinal scale compresses dynamically as a function of the local latitude
    deg_per_km_lon = deg_per_km_lat / math.cos(math.radians(center_lat))
    
    delta_lat = (height_km / 2.0) * deg_per_km_lat
    delta_lon = (width_km / 2.0) * deg_per_km_lon
    
    bounds = {
        "Target Core Center": (center_lat, center_lon),
        "NW Search Box Corner": (center_lat + delta_lat, center_lon - delta_lon),
        "NE Search Box Corner": (center_lat + delta_lat, center_lon + delta_lon),
        "SE Search Box Corner": (center_lat - delta_lat, center_lon + delta_lon),
        "SW Search Box Corner": (center_lat - delta_lat, center_lon - delta_lon),
        "COMPUTED AREA (KM2)": height_km * width_km
    }
    
    return bounds

# Run evaluation matching your target logs
results = calculate_geodesic_search_box(-32.9530, 92.9866, target_area_km2=4182.8)
for key, val in results.items():
    if isinstance(val, tuple):
        print(f"- {key} : {val[0]:.4f}°S, {val[1]:.4f}°E")
    else:
        print(f"- {key} : {val:.2f}")
