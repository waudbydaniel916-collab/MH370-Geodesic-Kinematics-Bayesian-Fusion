import os
import cdsapi
import copernicusmarine
from dotenv import load_dotenv

# Load standard environmental variables from your hidden local .env file
load_dotenv()

def download_historical_marine_currents(output_dir="./data"):
    """
    Automates the extraction of authentic GLORYS12V1 daily global ocean reanalysis 
    current matrices for March 2014 from the Copernicus Marine Service API.
    """
    print("Connecting to Copernicus Marine Service Data Store...")
    os.makedirs(output_dir, exist_ok=True)
    output_filepath = os.path.join(output_dir, "marine_currents_march2014.nc")
    
    # Retrieve the explicit keys from dotenv memory
    user_id = os.getenv("COPERNICUS_USERNAME")
    user_pass = os.getenv("COPERNICUS_PASSWORD")
    
    # Fallback check for service-specific variable names
    if not user_id:
        user_id = os.getenv("COPERNICUSMARINE_SERVICE_USERNAME")
        user_pass = os.getenv("COPERNICUSMARINE_SERVICE_PASSWORD")
        
    if not user_id or not user_pass:
        print("  Error: Credentials missing from the .env file.")
        print("  Ensure your .env file contains: COPERNICUS_USERNAME=GRIDLOCK")
        return None
    
    try:
        # Pass credentials explicitly into the subset function to bypass local cache prompts
        copernicusmarine.subset(
            dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
            variables=["uo", "vo"],
            start_datetime="2014-03-08T00:00:00",
            end_datetime="2014-03-31T23:59:59",
            minimum_longitude=80.0,
            maximum_longitude=105.0,
            minimum_latitude=-40.0,
            maximum_latitude=-25.0,
            output_directory=output_dir,
            output_filename="marine_currents_march2014.nc",
            username=user_id,
            password=user_pass
        )
        print(f"  Ocean current vectors successfully saved to: {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"  Copernicus Marine API request failed: {e}")
        return None

def download_historical_era5_winds(output_dir="./data"):
    """
    Automates the extraction of historical ECMWF ERA5 10m wind velocity fields
    for the target timeline using the Climate Data Store (CDS) API.
    """
    print("\nConnecting to ECMWF Climate Data Store...")
    os.makedirs(output_dir, exist_ok=True)
    output_filepath = os.path.join(output_dir, "era5_winds_march2014.nc")
    
    try:
        # Client handles the handshake using your local hidden ~/.cdsapirc file
        client = cdsapi.Client()
        client.retrieve(
            'reanalysis-era5-single-levels',
            {
                'product_type': 'reanalysis',
                'format': 'netcdf',
                'variable': [
                    '10m_u_component_of_wind', 
                    '10m_v_component_of_wind', 
                ],
                'year': '2014',
                'month': '03',
                'day': [
                    '08', '09', '10', '11', '12', '13', '14', '15'
                ],
                'time': [
                    '00:00', '03:00', '06:00', '09:00', '12:00', '15:00', '18:00', '21:00'
                ],
                'area': [
                    -25, 80, -40, 105, 
                ],
            },
            output_filepath
        )
        print(f"  Atmospheric wind vector matrices saved to: {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"  ECMWF CDS API request failed: {e}")
        return None

# ==========================================
# FILE EXECUTION DRIVER
# ==========================================
if __name__ == "__main__":
    print("  Initiating authentic weather grid sourcing sequence...")
    
    # 1. Run the Copernicus Marine extraction layer
    currents_file = download_historical_marine_currents()
    
    # 2. Run the ECMWF Climate Data Store layer
    winds_file = download_historical_era5_winds()
    
    print("\n  Data extraction pipeline completed.")




