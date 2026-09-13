import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os

def render_tactical_search_chart(csv_input_path, output_image_path="native_fusion_map.png"):
    """
    Generates a high-fidelity geographic plot of low, mid, and high windage
    debris trajectories along the 7th Arc using Cartopy coordinate mapping.
    """
    print(f"  Map Generator initialized. Reading particle track records from: '{csv_input_path}'")
    
    if not os.path.exists(csv_input_path):
        print(f"  Error: Cannot find '{csv_input_path}'. Run your swarm simulation first!")
        return None

    # Load the multi-class coordinate tracking dataset
    df = pd.read_csv(csv_input_path)
    
    # Establish a professional oceanographic plotting context
    plt.figure(figsize=(12, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    # Configure geographic spatial zoom window enclosing your search boundaries
    ax.set_extent([91.5, 94.5, -34.0, -31.5], crs=ccrs.PlateCarree())
    
    # Add base maritime mapping features
    ax.add_feature(cfeature.OCEAN, facecolor='#111b24')  # Slate dark ocean fill
    ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, color='gray', alpha=0.3)
    
    # Map colors to your specific asset morphology profiles
    color_map = {
        "low_windage": "#00ffcc",   # Bright Cyan for dense structural framing
        "mid_windage": "#ffcc00",   # Amber for cabin panel shards
        "high_windage": "#ff3366"   # Neon Pink for the high-buoyancy sail components
    }
    
    print("  Mapping coordinate nodes onto the spatial chart...")
    # Iteratively plot each separate fleet footprint array
    for current_class in df['leeway_class'].unique():
        sub_group = df[df['leeway_class'] == current_class]
        
        ax.scatter(
            sub_group['terminal_lon'], 
            sub_group['terminal_lat'], 
            color=color_map.get(current_class, 'white'),
            label=f"Debris Type: {current_class}", 
            alpha=0.7, 
            edgecolors='none',
            s=40,
            transform=ccrs.PlateCarree()
        )
        
    # Mark your pinpointed master fusion center coordinate
    master_target_lat = -32.8881
    master_target_lon = 92.9859
    ax.plot(
        master_target_lon, master_target_lat,
        marker='X', color='#ffffff', markersize=14, 
        markeredgecolor='#ff0000', markeredgewidth=2,
        label="PINPOINTED SEARCH TARGET (-32.8881°S, 92.9859°E)",
        transform=ccrs.PlateCarree()
    )
    
    # Style the master cartographic chart
    plt.title("MH370 Search Corridor Optimization Model\nMulti-Class Monte Carlo Ensemble Trajectories (March 2014)", 
              fontsize=14, pad=20, weight='bold', color='black')
    
    plt.legend(loc="lower left", framealpha=0.9, facecolor='#ffffff', edgecolor='none')
    
    # Save the output image payload to your repository folder
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"  Geographic target chart cleanly compiled and saved to: '{output_image_path}'")
    return output_image_path

if __name__ == "__main__":
    render_tactical_search_chart(csv_input_path="satellite_fused_weights.csv")
