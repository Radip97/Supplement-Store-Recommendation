# Re-load the required libraries after execution state reset
import json
import pandas as pd

# Reload the gym data file
gym_file_path = "gym.json"

# Read JSON file
with open(gym_file_path, "r", encoding="utf-8") as file:
    gym_data = json.load(file)

# Extract relevant details from gym JSON
gym_list = []
for element in gym_data["elements"]:
    tags = element.get("tags", {})
    gym_list.append({
        "ID": element.get("id"),
        "Name": tags.get("name", "Unknown"),
        "Latitude": element.get("lat"),
        "Longitude": element.get("lon")
    })

# Convert to DataFrame and save as CSV
gym_df = pd.DataFrame(gym_list)



# Clean the gym data by removing rows with 'Unknown' values in critical fields
clean_gym_df = gym_df.replace("Unknown", pd.NA).dropna(subset=["Name", "Latitude", "Longitude"])

# Save the cleaned data to a new CSV file
clean_gym_csv_path = "clean_gym_locations.csv"
clean_gym_df.to_csv(clean_gym_csv_path, index=False)





