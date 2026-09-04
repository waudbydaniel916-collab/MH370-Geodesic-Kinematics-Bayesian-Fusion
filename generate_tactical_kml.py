
import os
import pandas as pd

print("[SYSTEM] Compiling 3D Tactical KML Point Cloud Engine...")

base_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
manifest_path = os.path.join(base_dir, 'sonar_anomaly_manifest.csv')
kml_output_path = os.path.join(base_dir, 'mh370_debris_scatter.kml')

if os.path.exists(manifest_path):
    try:
        df = pd.read_csv(manifest_path)
        
        kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://opengis.net">
  <Document>
    <name>MH370 Shattered Debris Field Scatter Matrix</name>
    <Style id="neon_target">
      <IconStyle>
        <color>ff00ff00</color> <!-- Neon green target crosshairs -->
        <scale>1.3</scale>
        <Icon>
          <href>http://google.com</href>
        </Icon>
      </IconStyle>
    </Style>
"""
        
        # Loop through your 38 fragments to construct separate 3D map placemarks
        for _, row in df.iterrows():
            fid = int(row['Intercept_ID'])
            lat = row['Target_Latitude']
            lon = row['Target_Longitude']
            reflectivity = row['Acoustic_Reflectivity_Score'] * 100
            tag = row['Classification_Tag']
            
            kml_content += f"""    <Placemark>
      <name>Fragment #{fid:02d}</name>
      <description><![CDATA[
        <b>Classification:</b> {tag}<br/>
        <b>Intensity:</b> {reflectivity:.1f}% Reflection
      ]]></description>
      <styleUrl>#neon_target</styleUrl>
      <Point>
        <altitudeMode>relativeToSeafloor</altitudeMode>
        <coordinates>{lon},{lat},-5020</coordinates>
      </Point>
    </Placemark>
"""
            
        kml_content += """  </Document>
</kml>
"""
        
        with open(kml_output_path, 'w', encoding='utf-8') as f:
            f.write(kml_content)
            
        print(f"[SUCCESS] 3D Point-Cloud layer built cleanly at:\n ➔ {kml_output_path}\n")
        
    except Exception as e:
        print(f"[CRASH] Mapping array build failure: {e}")
else:
    print(f"[ERROR] Dependency missing: {manifest_path}. Run sonar_transfuser.py first.")


