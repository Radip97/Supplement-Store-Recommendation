import pandas as pd
import folium
from sklearn.cluster import DBSCAN
from geopy.distance import geodesic
from math import radians

# Load data
gyms = pd.read_csv('clean_gym_locations.csv')
stores = pd.read_csv('clean_supplement_store_locations.csv')

# ---------------------------
# DBSCAN Clustering
# ---------------------------
coords = gyms[['Latitude', 'Longitude']].applymap(radians).values
epsilon = 4.5 / 6371
db = DBSCAN(eps=epsilon, min_samples=3, algorithm='ball_tree', metric='haversine').fit(coords)
gyms['Cluster'] = db.labels_
gyms['IsClustered'] = gyms['Cluster'] != -1

# ---------------------------
# Recommendation Scoring
# ---------------------------
recommendations = []

for cluster_id in gyms['Cluster'].unique():
    if cluster_id == -1:
        continue

    gyms_in_cluster = gyms[gyms['Cluster'] == cluster_id]
    center_lat = gyms_in_cluster['Latitude'].mean()
    center_lon = gyms_in_cluster['Longitude'].mean()
    center = (center_lat, center_lon)

    # Gym stats
    gym_count = len(gyms_in_cluster)
    nearby_store_count = sum(
        geodesic(center, (store['Latitude'], store['Longitude'])).km <= 3
        for _, store in stores.iterrows()
    )
    spread_km = max(
        geodesic(center, (row['Latitude'], row['Longitude'])).km
        for _, row in gyms_in_cluster.iterrows()
    )
    
    # Manual density filter
    dense_gym_count = sum(
        geodesic(center, (row['Latitude'], row['Longitude'])).km <= 3
        for _, row in gyms_in_cluster.iterrows()
    )

    # Score formula
    score = (gym_count * 3) - (nearby_store_count * 2) - spread_km

    recommendations.append({
        'Cluster': cluster_id,
        'Latitude': center_lat,
        'Longitude': center_lon,
        'Gym_Count': gym_count,
        'Nearby_Store_Count': nearby_store_count,
        'Dense_Gym_Count': dense_gym_count,
        'Spread_km': spread_km,
        'Score': score
    })

recommend_df = pd.DataFrame(recommendations)

# ---------------------------
# Filter & Final Selection
# ---------------------------
# Manual cutoff to exclude St. Francisville and rural zones
# Exclude rural outliers
recommend_df = recommend_df[recommend_df['Latitude'] < 30.6]

# Try strict filter first
final_recommend = recommend_df[
    (recommend_df['Gym_Count'] >= 6) &
    (recommend_df['Dense_Gym_Count'] >= 5) &
    (recommend_df['Spread_km'] <= 4.5)
]

# If not enough, relax slightly
if len(final_recommend) < 5:
    final_recommend = recommend_df[
        (recommend_df['Gym_Count'] >= 5) &
        (recommend_df['Dense_Gym_Count'] >= 4) &
        (recommend_df['Spread_km'] <= 6)
    ]

# If still not enough, allow even looser spread but still dense
if len(final_recommend) < 5:
    final_recommend = recommend_df[
        (recommend_df['Gym_Count'] >= 4) &
        (recommend_df['Dense_Gym_Count'] >= 3) &
        (recommend_df['Spread_km'] <= 7)
    ]

# Fallback to top 5 by score if needed
if len(final_recommend) < 5:
    final_recommend = recommend_df.sort_values(by='Score', ascending=False).head(5)

# Final sort for display
final_recommend = final_recommend.sort_values(by='Score', ascending=False).head(10)


# ---------------------------
# Map Visualization
# ---------------------------
map_center = [gyms['Latitude'].mean(), gyms['Longitude'].mean()]
m = folium.Map(location=map_center, zoom_start=9)

# Plot gyms
for _, row in gyms.iterrows():
    color = 'blue' if row['IsClustered'] else 'lightgray'
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Gym: {row['Name']}",
        icon=folium.Icon(color=color, icon='dumbbell', prefix='fa')
    ).add_to(m)

# Plot stores
for _, row in stores.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"Store: {row['Name']}",
        icon=folium.Icon(color='green', icon='shopping-cart', prefix='fa')
    ).add_to(m)

# Plot recommendations
for i, (_, row) in enumerate(final_recommend.iterrows(), start=1):
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=(f"📍 Recommendation #{i}\n"
               f"Gyms: {row['Gym_Count']}\n"
               f"Stores Nearby: {row['Nearby_Store_Count']}\n"
               f"Spread: {row['Spread_km']:.2f} km"),
        icon=folium.Icon(color='red', icon='plus-sign')
    ).add_to(m)

# Save map
m.save("smart_recommendation_map.html")

