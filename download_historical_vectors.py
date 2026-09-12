import os
import cdsapi
import copernicusmarine
# Import the dotenv library to load hidden configurations
from dotenv import load_dotenv

# Load the environment keys from the local hidden .env file
load_dotenv()

def download_historical_marine_currents(output_dir="./data"):
    """
    Automates the extraction of authentic GLORYS12V1 daily global ocean reanalysis 
    current matrices for March 2014 from the Copernicus Marine Service API.
    """
    print("  Connecting to Copernicus Marine Service Data Store...")
    os.makedirs(output_dir, exist_ok=True)
    output_filepath = os.path.join(output_dir, "marine_currents_march2014.nc")
    
    # Securely retrieve credentials out of system memory
    user_id = os.getenv("COPERNICUS_USERNAME")
    user_pass = os.getenv("COPERNICUS_PASSWORD")
    
    if not user_id or not user_pass:
        print(" Error: Missing credentials. Ensure COPERNICUS_USERNAME and COPERNICUS_PASSWORD are set in your hidden .env file.")
        return None
    
    try:
        copernicusmarine.subset(
            dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
            variables=["uo", "vo"],
            start_date="2014-03-08T00:00:00",
            end_date="2014-03-31T23:59:59",
            minimum_longitude=80.0,
            maximum_longitude=105.0,
            minimum_latitude=-40.0,
            maximum_latitude=-25.0,
            output_directory=output_dir,
            output_filename="marine_currents_march2014.nc",
            force_download=True,
            
            # Securely pass the hidden runtime configurations
            username=user_id,
            password=user_pass
        )
        print(f"  Ocean current vectors successfully saved to: {output_filepath}")
        return output_filepath
    except Exception as e:
        print(f"  Copernicus Marine API request failed: {e}")
        return None

# The rest of your script (for ERA5 winds) stays exactly the same...
