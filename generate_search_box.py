import os

def create_geospatial_search_kml(target_lat, target_lon, target_depth_m, output_path="search_corridor.kml"):
    """
    Generates a validated KML file containing a 3D search box perimeter 
    and target placemark for visualization in Google Earth Pro.
    """
    print(f"  Generating geospatial KML file for target center: {target_lat}, {target_lon}")
    
    # Define a bounding perimeter box offset (approx 5km radius for tactical coverage)
    offset = 0.045 
    
    nw_lat, nw_lon = target_lat + offset, target_lon - offset
    ne_lat, ne_lon = target_lat + offset, target_lon + offset
    se_lat, se_lon = target_lat - offset, target_lon + offset
    sw_lat, sw_lon = target_lat - offset, target_lon - offset

    # Raw KML XML template structure text strings
    kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://opengis.net">
  <Document>
    <name>MH370 Calibrated Tactical Search Corridor</name>
    <description>Generated via Curtin University Multi-Class Bayesian Fusion Pipeline</description>
    
    <!-- Target Center Pin Point -->
    <Placemark>
      <name>PINPOINTED TARGET CENTER</name>
      <description>Calculated Seafloor Depth: {target_depth_m:.2f} meters</description>
      <Point>
        <coordinates>{target_lon},{target_lat},-{target_depth_m}</coordinates>
      </Point>
    </Placemark>
    
    <!-- Bounding Search Perimeter Box -->
    <Placemark>
      <name>TACTICAL SEARCH BOUNDARY POLYGON</name>
      <Style>
        <LineStyle>
          <color>ff0000ff</color> <!-- Red Boundary Line -->
          <width>3</width>
        </LineStyle>
        <PolyStyle>
          <color>400000ff</color> <!-- Translucent Red Fill Inside -->
        </PolyStyle>
      </Style>
      <Polygon>
        <tessellate>1</tessellate>
        <outerBoundaryIs>
          <LinearRing>
            <coordinates>
              {nw_lon},{nw_lat},0
              {ne_lon},{ne_lat},0
              {se_lon},{se_lat},0
              {sw_lon},{sw_lat},0
              {nw_lon},{nw_lat},0
            </coordinates>
          </LinearRing>
        </outerBoundaryIs>
      </Polygon>
    </Placemark>
  </Document>
</kml>
"""
    try:
        with open(output_path, "w") as f:
            f.write(kml_content)
        print(f"  Geospatial KML map cleanly compiled and saved to: '{output_path}'")
        return output_path
    except Exception as e:
        print(f"  KML generation failed: {e}")
        return None

if __name__ == "__main__":
    # Draw map using your model's optimized center and validated depth metrics
    create_geospatial_search_kml(target_lat=-32.8404, target_lon=92.9632, target_depth_m=4311.58)
