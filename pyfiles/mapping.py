import pandas as pd
import folium

# Load the datasets
gyms_df = pd.read_csv('clean_gym_locations.csv')  # Replace with your actual gym file path
stores_df = pd.read_csv('clean_supplement_store_locations.csv')  # Replace with your actual store file path

# Center the map around the average location
avg_lat = pd.concat([gyms_df['Latitude'], stores_df['Latitude']]).mean()
avg_lon = pd.concat([gyms_df['Longitude'], stores_df['Longitude']]).mean()
map_center = [avg_lat, avg_lon]

# Create a folium map
m = folium.Map(location=map_center, zoom_start=12)

# Add gyms to the map
for _, row in gyms_df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Gym: {row['Name']}",
        icon=folium.Icon(color='blue', icon='dumbbell', prefix='fa')
    ).add_to(m)

# Add supplement stores to the map
for _, row in stores_df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Store: {row['Name']}",
        icon=folium.Icon(color='green', icon='shopping-cart', prefix='fa')
    ).add_to(m)

# Save the map to an HTML file
m.save("gym_store_map.html")
