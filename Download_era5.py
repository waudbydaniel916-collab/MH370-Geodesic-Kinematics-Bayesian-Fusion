import cdsapi

print("[SYSTEM] Initializing Official ECMWF ERA5 Downloader...")
c = cdsapi.Client()

# This script requests a strictly cropped geographic box over the Indian Ocean 
# for March 2014 to keep the file size tiny and save your storage space.
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            '10m_u_component_of_wind', 
            '10m_v_component_of_wind'
        ],
        'year': '2014',
        'month': '03',
        'day': [
            '08', '09', '10', '11', '12', 
            '13', '14', '15', '16', '17', '18'
        ],
        'time': [
            '00:00', '06:00', '12:00', '18:00'
        ],
        # Strict Bounding Box Crop: North, West, South, East (Indian Ocean Window Only)
        'area': [0, 30, -45, 115], 
    },
    '/Users/charlottewaudby/Documents/7ThArc/historical_winds_2014.nc'
)

print("[SUCCESS] Operational ERA5 NetCDF file downloaded cleanly.")

