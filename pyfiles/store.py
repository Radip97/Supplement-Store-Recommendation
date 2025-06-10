import json
import pandas as pd

supplement_file_path = "supplement store.json"


with open(supplement_file_path, "r", encoding="utf-8") as file:
    supplement_data = json.load(file)

supplement_list = []
for element in supplement_data["elements"]:
    tags = element.get("tags", {})
    supplement_list.append({
        "ID": element.get("id"),
        "Name": tags.get("name", "Unknown"),
        "Latitude": element.get("lat") if "lat" in element else element.get("center", {}).get("lat"),
        "Longitude": element.get("lon") if "lon" in element else element.get("center", {}).get("lon")
    })


supplement_df = pd.DataFrame(supplement_list)

clean_supplement_df = supplement_df.replace("Unknown", pd.NA).dropna(subset=["Name", "Latitude", "Longitude"])

clean_supplement_csv_path = "clean_supplement_store_locations.csv"
clean_supplement_df.to_csv(clean_supplement_csv_path, index=False)


