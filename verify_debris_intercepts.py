import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET

def parse_kml_debris_coordinates(kml_filepath):
    """
    Parses the actual historical beach debris discovery sites from the KML file
    to use as baseline verification targets.
    """
    print(f"  Parsing historical debris coordinates from: '{kml_filepath}'")
    
    # Standard KML XML namespace parser
    namespaces = {'kml': 'http://opengis.net'}
    tree = ET.parse(kml_filepath)
    root = tree.getroot()
    
    parsed_sites = []
    
    # Locate all Placemarks containing physical debris coordinates
    for placemark in root.findall('.//kml:Placemark', namespaces):
        name_node = placemark.find('kml:name', namespaces)
        coord_node = placemark.find('.//kml:coordinates', namespaces)
        
        if name_node is not None and coord_node is not None:
            coord_text = coord_node.text.strip().split(',')
            # KML format stores data as: Longitude, Latitude, Elevation
            lon = float(coord_text[0])
            lat = float(coord_text[1])
            parsed_sites.append({'debris_name': name_node.text, 'target_lat': lat, 'target_lon': lon})
            
    return pd.DataFrame(parsed_sites)

def cross_validate_drift_trajectories(bayesian_results_path, debris_kml_path):
    """
    Calculates the spatial variance vector between your model's outputs
    and historical physical discoveries.
    """
    debris_df = parse_kml_debris_coordinates(debris_kml_path)
    
    try:
        swarm_df = pd.read_csv(bayesian_results_path)
    except FileNotFoundError:
        print("  Error: Run your swarm simulation first to generate bayesian_results.csv")
        return

    print("\n========================================================")
    print("  HISTORICAL DEBRIS TRACKING VECTOR CHECK")
    print("========================================================")
    
    # Filter for high-windage items (like the flaperon) which travel long distances
    high_windage_swarm = swarm_df[swarm_df['leeway_class'] == 'high_windage']
    
    if high_windage_swarm.empty:
        # Fallback if processing older single-fleet files
        high_windage_swarm = swarm_df

    # Extract our simulated terminal footprint center
    sim_lat = high_windage_swarm['terminal_lat'].mean()
    sim_lon = high_windage_swarm['terminal_lon'].mean()
    
    for _, row in debris_df.iterrows():
        # Compute macro spatial angular offset errors across the Indian Ocean basin
        lat_error = sim_lat - row['target_lat']
        lon_error = sim_lon - row['target_lon']
        angular_distance = np.sqrt(lat_error**2 + lon_error**2)
        
        print(f"  Item: {row['debris_name']:<18}")
        print(f"   Trajectory Offset Variance: {angular_distance:.2f} degrees from simulated path.")
    print("========================================================")

if __name__ == "__main__":
    # Run verification check across your files
    cross_validate_drift_trajectories(
        bayesian_results_path="bayesian_results.csv",
        debris_kml_path="mh370_debris_scatter.kml"
    )
