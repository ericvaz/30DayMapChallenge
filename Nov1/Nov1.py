import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from pyproj import Transformer


#Earthquakes for Iberian Peninsula
earthquakes = pd.read_csv(your_file_path_here/Eartquakes-1990-2023.csv)

iberian_earthquakes = earthquakes[
    (earthquakes['latitude'] >= 36.0) & (earthquakes['latitude'] <= 44.0) &
    (earthquakes['longitude'] >= -9.5) & (earthquakes['longitude'] <= 3.5)
]
min_magnitude = 2.0
iberian_earthquakes = iberian_earthquakes[iberian_earthquakes['magnitudo'] >= min_magnitude]


# Remove outliers based on IQR for latitude and longitude
q1_lat = iberian_earthquakes['latitude'].quantile(0.25)
q3_lat = iberian_earthquakes['latitude'].quantile(0.75)
iqr_lat = q3_lat - q1_lat
lat_min = q1_lat - 1.5 * iqr_lat
lat_max = q3_lat + 1.5 * iqr_lat
