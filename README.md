# MH370 Geodesic Kinematics & Bayesian Fusion Model

This repository implements a multivariate Bayesian Data Fusion framework combined with a 4th-Order Runge-Kutta (RK4) Lagrangian advection solver to optimize search corridors for missing flight MH370 along the historical 7th Arc baseline. 

The model systematically reduces the unconstrained search boundary by integrating independent datasets—including satellite communications, deep-sea hydroacoustics, drift kinematics, and biological markers—into a unified Joint Probability Density Function (PDF).

## Architectural Framework & Sensor Inputs

The probability engine isolates the absolute mathematical peak convergence zone on the WGS84 ellipsoid by multiplying independent spatial probabilities:

P_fused = P_drift * P_satellite * P_barnacle * P_acoustic

### 1. Kinematic Drift Model (P_drift)
The system executes a vectorized Runge-Kutta 4th-Order solver that steps floating debris particles through historical environmental reanalysis grids. The solver parses real temporal NetCDF matrices containing zonal and meridional current components alongside 10-meter wind vectors. Local degree scaling calculations account for the oblate convergence of meridians near the sub-Antarctic latitudes.

### 2. Satellite Doppler Tracking (P_satellite)
The satellite alignment layer evaluates particle coordinates against historical Inmarsat transmission logs. It applies a Gaussian Probability Density Function to score particle trajectories based on their mathematical alignment with the final recorded 177.80 Hz Burst Frequency Offset (BFO) Doppler curves.

### 3. Biological Sclerochronology Constraints (P_barnacle)
Oxygen isotope ratios and thermal growth profiles from recovered physical debris constrain the final months of the drift window to cooler southern waters. The framework models an operational probability drop-off for coordinate spaces north of -31.5°S based on marine barnacle growth thresholds.

### 4. Hydroacoustic Waveguide Propagation (P_acoustic)
Underwater impact acoustic wave modeling discards simple vertical water column velocity averages. Wave propagation times are integrated horizontally directly along the deep-ocean SOFAR channel axis depth layer (1,000 meters) to calculate travel-time vectors and inter-station delays to listening stations HA01 and H08.

## Pipeline Optimization Output

The localized execution driver resolves the multivariate data matrix using a high-capacity Monte Carlo ensemble swarm, yielding updated search parameters including a targeted center at `-35.0269°S, 90.0139°E` and an active processing size of `1,000` particles. For the complete markdown block details, please refer to the referenced repository documentation.

## Repository File Structure

* stochastic_drift.py: Core RK4 advection solver engine linking coordinate updates to spatial NetCDF variable keys.
* run_swarm_simulation.py: Monte Carlo wrapper executing parallel particle tracking sequences forward through time.
* evaluate_satellite_bfo.py: Statistical Gaussian wrapper validating Doppler frequency offsets.
* fused_probability_engine.py: Master joint probability matrix compiler executing the final Bayesian multiplication loop.

## Dependencies

The tracking pipeline requires the following Python libraries for data processing and matrix operations:
* numpy
* pandas
* xarray
* scipy
* netCDF4

## Pipeline Execution and Replicability Guide

Follow this sequential pipeline execution path to reproduce the multi-sensor data fusion calculations and generate the optimized target matrix payloads.

### 1. Configure the Environmental Data Store Keys
Isolate your network credentials by creating a local environment file named `.env` in the root directory. This keeps your personal weather portal login keys hidden from the public repository branch. Add your access strings to the file layout as follows:
```text
COPERNICUS_USERNAME=your_username
COPERNICUS_PASSWORD=your_password
```
Additionally, ensure your personal Climate Data Store token is saved inside your operating system's home directory file template at `~/.cdsapirc` to satisfy the ECMWF validation checks.

### 2. Execute the Data Ingestion Phase
Run the weather download script to pull authentic historical atmospheric and oceanographic reanalysis matrices. This bypasses simulated parameters by fetching the verified weather grids from March 2014:
```bash
python download_historical_vectors.py
```
This command successfully saves the verified historical winds file (`era5_winds_march2014.nc`) straight into your local data folder.

### 3. Initialize the Multi-Class Particle Solver
Run the Monte Carlo fleet swarm tracking routine. This distributes an array of parallel particles along the candidate 7th Arc points and advects them through time using your 4th-Order Runge-Kutta equations:
```bash
python run_swarm_simulation.py
```
This process automatically segregates trajectories by their distinct windage traits and records the terminal locations into `bayesian_results.csv`.

### 4. Apply the Satellite Doppler Calibration
Execute the satellite data verification code block. This parses your new drift database and calculates the relative velocity lines against the orbital paths of the moving Inmarsat-3F1 satellite:
```bash
python evaluate_satellite_bfo.py
```
This script runs a Gaussian probability distribution filter, scoring each tracking path against the historical 177.80 Hz Doppler curves and saving the arrays to `satellite_fused_weights.csv`.

### 5. Compile the Master Bayesian Fusion Matrix
Run the ultimate multivariate data fusion engine. This combines your wind tracking logs with your biological barnacle threshold constraints and your dynamic vertical SOFAR channel wave shoaling profiles:
```bash
python fused_probability_engine.py
```
The master engine multiplies all active probability layers together, handles the spatial array scaling, and prints your finalized optimized search coordinates directly to the console window.

### 6. Generate Geospatial Map and Depth Profiles
To verify the seafloor terrain constraints and export your targets into standalone geographic map overlays for mapping programs like Google Earth Pro or ArcGIS, run the final verification modules:
```bash
python validate_target_depth.py
python generate_search_box.py
python generate_search_map.py
```
These finalize your investigation payload by exporting a 3D Keyhole Markup file (`search_corridor.kml`) alongside a crisp geographic tracking layout (`native_fusion_map.png`).
