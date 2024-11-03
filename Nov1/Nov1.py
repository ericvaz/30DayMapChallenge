import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from pyproj import Transformer

# Load the CSV file
earthquakes = pd.read_csv('iberianearthquakes.csv')

# Filter data for earthquakes within the Iberian Peninsula
iberian_earthquakes = earthquakes[
    (earthquakes['latitude'] >= 36.0) & (earthquakes['latitude'] <= 44.0) &
    (earthquakes['longitude'] >= -9.5) & (earthquakes['longitude'] <= 3.5)
]
min_magnitude = 2.0
iberian_earthquakes = iberian_earthquakes[iberian_earthquakes['magnitudo'] >= min_magnitude]

q1_lat = iberian_earthquakes['latitude'].quantile(0.25)
q3_lat = iberian_earthquakes['latitude'].quantile(0.75)
iqr_lat = q3_lat - q1_lat
lat_min = q1_lat - 1.5 * iqr_lat
lat_max = q3_lat + 1.5 * iqr_lat

q1_lon = iberian_earthquakes['longitude'].quantile(0.25)
q3_lon = iberian_earthquakes['longitude'].quantile(0.75)
iqr_lon = q3_lon - q1_lon
lon_min = q1_lon - 1.5 * iqr_lon
lon_max = q3_lon + 1.5 * iqr_lon

filtered_earthquakes = iberian_earthquakes[
    (iberian_earthquakes['latitude'] >= lat_min) &
    (iberian_earthquakes['latitude'] <= lat_max) &
    (iberian_earthquakes['longitude'] >= lon_min) &
    (iberian_earthquakes['longitude'] <= lon_max)
]

# GeoDataFrame for the earthquake data and set it to EPSG:3857
gdf = gpd.GeoDataFrame(
    filtered_earthquakes,
    geometry=gpd.points_from_xy(filtered_earthquakes['longitude'], filtered_earthquakes['latitude']),
    crs="EPSG:4326"
).to_crs("EPSG:3857")

# Load the Iberian Peninsula shapefile as a basemap and reproject it to EPSG:3857 
iberia_basemap = gpd.read_file('iberia.shp').to_crs("EPSG:3857")

# Calculate extent limits in EPSG:3857 for the earthquake points and plot
x_min, y_min, x_max, y_max = gdf.total_bounds
fig, ax = plt.subplots(figsize=(10, 8), facecolor="black")  # Set the entire figure background to black

# Set the background color of the plot area to black
ax.set_facecolor("black")

# Plot the Iberian Peninsula shapefile with a white outline and no fill
iberia_basemap.plot(ax=ax, color="none", edgecolor="white", linewidth=0.5)
sns.scatterplot(
    data=gdf,
    x=gdf.geometry.x, y=gdf.geometry.y,
    hue='magnitudo',  # Color by magnitude
    palette="Spectral",  # Use a vibrant palette that stands out on black
    size='magnitudo',  # Size points by magnitude
    sizes=(10, 200),  # Adjust min and max point sizes
    alpha=0.3,  # Increase transparency for the points
    edgecolor= '#e5dfda',  # White edge around the points for contrast
    linewidth=0.2,
    legend="brief",
    ax=ax
)
ax.set_xlim([x_min, x_max])
ax.set_ylim([y_min, y_max])

# Some minor tweaks
plt.title("Earthquake Magnitude Distribution in the Iberian Peninsula (1920 to 2023)", color="white")
plt.xlabel("Longitude (Projected in EPSG:3857)", color="white")
plt.ylabel("Latitude (Projected in EPSG:3857)", color="white")
legend = plt.legend(title='Magnitude', loc='upper right', facecolor="black", edgecolor="white", fontsize='medium')
for text in legend.get_texts():
    text.set_color("white")  # Set legend text color to white
legend.get_title().set_color("white")  # Set legend title color to white
plt.grid(True, linestyle='--', color='grey', alpha=0.8)  # Set grid transparency to 50%
ax.tick_params(colors='white')  # Set tick colors to white for readability

# Show the plot
plt.show()
